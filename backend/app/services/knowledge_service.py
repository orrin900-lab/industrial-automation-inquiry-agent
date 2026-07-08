from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.rag.build_qdrant_index import build_qdrant_index
from app.rag.embeddings import HashingEmbeddingProvider
from app.rag.loader import load_markdown_documents
from app.rag.qdrant_store import QdrantStore, QdrantStoreError
from app.rag.splitter import split_markdown_documents
from app.schemas.knowledge import (
    KnowledgeChunkItem,
    KnowledgeChunksResponse,
    KnowledgeReindexResponse,
    KnowledgeStatusResponse,
)
from app.utils.config import AppConfig, get_config


def get_knowledge_status(config: AppConfig | None = None) -> KnowledgeStatusResponse:
    resolved_config = config or get_config()
    source_files, local_chunks_count = _local_knowledge_summary(resolved_config)
    points_count: int | None = None
    qdrant_available = False
    error_message: str | None = None

    if resolved_config.rag.enable_qdrant_rag:
        try:
            store = _create_qdrant_store(resolved_config)
            collection_info = store.get_collection_info()
            qdrant_available = collection_info is not None
            if qdrant_available:
                points_count = store.get_points_count()
        except Exception as exc:
            error_message = _safe_error(exc)

    return KnowledgeStatusResponse(
        rag_mode=(
            "qdrant"
            if resolved_config.rag.use_qdrant and qdrant_available
            else "keyword_fallback"
            if resolved_config.rag.use_qdrant
            else "keyword"
        ),
        qdrant_enabled=resolved_config.rag.enable_qdrant_rag,
        qdrant_available=qdrant_available,
        collection_name=resolved_config.rag.qdrant_collection,
        points_count=points_count,
        vector_size=resolved_config.rag.qdrant_vector_size,
        indexed_chunks=points_count or 0,
        source_files=source_files,
        fallback_available=True,
        embedding_provider="deterministic_hashing",
        last_checked_at=datetime.now(UTC).isoformat(),
        error_message=error_message,
    )


def list_knowledge_chunks(
    *,
    limit: int = 20,
    offset: int = 0,
    source_file: str | None = None,
    config: AppConfig | None = None,
) -> KnowledgeChunksResponse:
    resolved_config = config or get_config()
    safe_limit = max(1, min(limit, 100))
    safe_offset = max(0, offset)

    if not resolved_config.rag.enable_qdrant_rag:
        return KnowledgeChunksResponse(
            items=[],
            total=0,
            limit=safe_limit,
            offset=safe_offset,
            source_file=source_file,
            error_message="Qdrant RAG is disabled; chunk listing requires Qdrant.",
        )

    try:
        store = _create_qdrant_store(resolved_config)
        points, total = store.scroll_payloads(
            limit=safe_limit,
            offset=safe_offset,
            source_file=source_file,
        )
    except Exception as exc:
        return KnowledgeChunksResponse(
            status="error",
            items=[],
            total=0,
            limit=safe_limit,
            offset=safe_offset,
            source_file=source_file,
            error_message=f"Failed to load Qdrant chunks: {_safe_error(exc)}",
        )

    return KnowledgeChunksResponse(
        items=[_point_to_chunk_item(point) for point in points],
        total=total,
        limit=safe_limit,
        offset=safe_offset,
        source_file=source_file,
    )


def rebuild_knowledge_index(
    config: AppConfig | None = None,
) -> KnowledgeReindexResponse:
    resolved_config = config or get_config()
    if not resolved_config.rag.enable_qdrant_rag:
        return KnowledgeReindexResponse(
            success=False,
            collection_name=resolved_config.rag.qdrant_collection,
            message="Qdrant RAG is disabled; index rebuild was not executed.",
            error_message="ENABLE_QDRANT_RAG=false",
        )

    try:
        result = build_qdrant_index(resolved_config)
    except (QdrantStoreError, OSError, ValueError, RuntimeError) as exc:
        return KnowledgeReindexResponse(
            success=False,
            collection_name=resolved_config.rag.qdrant_collection,
            message="Failed to rebuild Qdrant index.",
            error_message=_safe_error(exc),
        )

    return KnowledgeReindexResponse(
        success=True,
        collection_name=result.collection_name,
        indexed_chunks=result.chunks_upserted,
        points_count=result.points_count,
        message="Qdrant index rebuilt successfully.",
    )


def _create_qdrant_store(config: AppConfig) -> QdrantStore:
    return QdrantStore(
        url=config.rag.qdrant_url,
        collection_name=config.rag.qdrant_collection,
        vector_size=config.rag.qdrant_vector_size,
        embedding_provider=HashingEmbeddingProvider(config.rag.qdrant_vector_size),
        timeout_seconds=config.rag.qdrant_timeout_seconds,
    )


def _local_knowledge_summary(config: AppConfig) -> tuple[list[str], int]:
    documents = load_markdown_documents(
        [
            config.faq_md,
            config.selection_rules_md,
            config.email_templates_md,
        ]
    )
    chunks = split_markdown_documents(documents)
    return [document.source_file for document in documents], len(chunks)


def _point_to_chunk_item(point: dict[str, Any]) -> KnowledgeChunkItem:
    payload = point.get("payload") or {}
    content = str(payload.get("content") or "")
    return KnowledgeChunkItem(
        chunk_id=str(payload.get("chunk_id") or point.get("id") or ""),
        source_file=str(payload.get("source_file") or "unknown"),
        section_title=str(payload.get("section_title") or "section"),
        document_type=str(payload.get("document_type") or "markdown"),
        content_preview=_preview(content),
        content=content,
        score=None,
    )


def _preview(content: str, max_chars: int = 300) -> str:
    normalized = " ".join(content.split())
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max_chars - 3].rstrip() + "..."


def _safe_error(exc: Exception) -> str:
    return str(exc).replace("\n", " ").strip()

