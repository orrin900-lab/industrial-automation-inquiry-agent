from __future__ import annotations

import json
import re
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from uuid import uuid5, NAMESPACE_URL

from app.rag.embeddings import EmbeddingProvider
from app.rag.loader import KnowledgeChunk, KnowledgeMetadata, RetrievedKnowledge


class QdrantStoreError(RuntimeError):
    pass


class QdrantStore:
    """Small REST client for Qdrant used by the prototype backend."""

    def __init__(
        self,
        *,
        url: str,
        collection_name: str,
        vector_size: int,
        embedding_provider: EmbeddingProvider,
        timeout_seconds: float = 3.0,
    ) -> None:
        self.url = url.rstrip("/")
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.embedding_provider = embedding_provider
        self.timeout_seconds = timeout_seconds

    def ensure_collection(self) -> None:
        existing = self._get_collection()
        if existing:
            existing_size = _extract_vector_size(existing)
            if existing_size and existing_size != self.vector_size:
                raise QdrantStoreError(
                    "Qdrant collection vector size mismatch: "
                    f"expected {self.vector_size}, got {existing_size}."
                )
            return

        self._request(
            "PUT",
            f"/collections/{quote(self.collection_name)}",
            {
                "vectors": {
                    "size": self.vector_size,
                    "distance": "Cosine",
                }
            },
        )

    def upsert_chunks(self, chunks: list[KnowledgeChunk]) -> int:
        if not chunks:
            return 0
        self.ensure_collection()
        points = []
        vectors = self.embedding_provider.embed_documents(
            [chunk.content for chunk in chunks]
        )
        for chunk, vector in zip(chunks, vectors, strict=True):
            points.append(
                {
                    "id": str(uuid5(NAMESPACE_URL, chunk.metadata.chunk_id)),
                    "vector": vector,
                    "payload": {
                        "content": chunk.content,
                        "source_file": chunk.metadata.source_file,
                        "section_title": chunk.metadata.section_title,
                        "document_type": chunk.metadata.document_type,
                        "chunk_id": chunk.metadata.chunk_id,
                    },
                }
            )

        self._request(
            "PUT",
            f"/collections/{quote(self.collection_name)}/points?wait=true",
            {"points": points},
        )
        return len(points)

    def search(self, query: str, top_k: int = 4) -> list[RetrievedKnowledge]:
        self.ensure_collection()
        response = self._request(
            "POST",
            f"/collections/{quote(self.collection_name)}/points/search",
            {
                "vector": self.embedding_provider.embed_text(query),
                "limit": top_k,
                "with_payload": True,
            },
        )
        results = response.get("result", [])
        if not isinstance(results, list):
            raise QdrantStoreError("Qdrant search returned an invalid result payload.")

        retrieved: list[RetrievedKnowledge] = []
        for item in results:
            payload = item.get("payload") or {}
            metadata = KnowledgeMetadata(
                source_file=str(payload.get("source_file", "unknown")),
                section_title=str(payload.get("section_title", "section")),
                document_type=str(payload.get("document_type", "markdown")),
                chunk_id=str(payload.get("chunk_id", "")),
            )
            content = str(payload.get("content", ""))
            retrieved.append(
                RetrievedKnowledge(
                    content=content,
                    score=_hybrid_score(query, content, metadata, item.get("score", 0.0)),
                    metadata=metadata,
                )
            )
        retrieved.sort(key=lambda result: result.score, reverse=True)
        return retrieved

    def _get_collection(self) -> dict[str, Any] | None:
        try:
            return self._request("GET", f"/collections/{quote(self.collection_name)}")
        except QdrantStoreError as exc:
            if "HTTP 404" in str(exc):
                return None
            raise

    def _request(
        self, method: str, path: str, payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        body = None
        headers = {"Content-Type": "application/json"}
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")

        request = Request(
            self.url + path,
            data=body,
            headers=headers,
            method=method,
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
        except HTTPError as exc:
            details = exc.read().decode("utf-8", errors="ignore")
            raise QdrantStoreError(f"Qdrant HTTP {exc.code}: {details}") from exc
        except URLError as exc:
            raise QdrantStoreError(f"Qdrant connection failed: {exc.reason}") from exc
        except OSError as exc:
            raise QdrantStoreError(f"Qdrant request failed: {exc}") from exc

        if not raw:
            return {}
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise QdrantStoreError("Qdrant returned non-JSON response.") from exc


def _extract_vector_size(collection_response: dict[str, Any]) -> int | None:
    result = collection_response.get("result") or {}
    config = result.get("config") or {}
    params = config.get("params") or {}
    vectors = params.get("vectors") or {}
    if isinstance(vectors, dict) and "size" in vectors:
        return int(vectors["size"])
    if isinstance(vectors, dict):
        for vector_config in vectors.values():
            if isinstance(vector_config, dict) and "size" in vector_config:
                return int(vector_config["size"])
    return None


def _normalize_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    return round(max(0.0, min(1.0, score)), 3)


def _hybrid_score(
    query: str,
    content: str,
    metadata: KnowledgeMetadata,
    vector_score: Any,
) -> float:
    query_terms = set(_tokenize(query))
    haystack_terms = set(
        _tokenize(
            " ".join(
                [
                    content,
                    metadata.source_file,
                    metadata.section_title,
                    metadata.document_type,
                ]
            )
        )
    )
    if not query_terms:
        lexical_score = 0.0
    else:
        lexical_score = len(query_terms & haystack_terms) / max(len(query_terms), 1)
    combined = _normalize_score(vector_score) * 0.7 + min(1.0, lexical_score) * 0.3
    return round(max(0.0, min(1.0, combined)), 3)


def _tokenize(text: str) -> list[str]:
    return [token for token in re.findall(r"[\w]+", text.lower()) if len(token) > 2]
