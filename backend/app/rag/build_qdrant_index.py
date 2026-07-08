from __future__ import annotations

from dataclasses import dataclass

from app.rag.embeddings import HashingEmbeddingProvider
from app.rag.loader import load_markdown_documents
from app.rag.qdrant_store import QdrantStore
from app.rag.splitter import split_markdown_documents
from app.utils.config import AppConfig, get_config


@dataclass(frozen=True)
class QdrantIndexBuildResult:
    collection_name: str
    chunks_loaded: int
    chunks_upserted: int
    qdrant_url: str
    points_count: int


def build_qdrant_index(config: AppConfig | None = None) -> QdrantIndexBuildResult:
    resolved_config = config or get_config()
    documents = load_markdown_documents(
        [
            resolved_config.faq_md,
            resolved_config.selection_rules_md,
            resolved_config.email_templates_md,
        ]
    )
    chunks = split_markdown_documents(documents)
    store = QdrantStore(
        url=resolved_config.rag.qdrant_url,
        collection_name=resolved_config.rag.qdrant_collection,
        vector_size=resolved_config.rag.qdrant_vector_size,
        embedding_provider=HashingEmbeddingProvider(
            resolved_config.rag.qdrant_vector_size
        ),
        timeout_seconds=resolved_config.rag.qdrant_timeout_seconds,
    )
    upserted = store.upsert_chunks(chunks)
    points_count = store.get_points_count()
    return QdrantIndexBuildResult(
        collection_name=resolved_config.rag.qdrant_collection,
        chunks_loaded=len(chunks),
        chunks_upserted=upserted,
        qdrant_url=resolved_config.rag.qdrant_url,
        points_count=points_count,
    )
