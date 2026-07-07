from functools import cached_property
from typing import Any

from app.rag.embeddings import HashingEmbeddingProvider
from app.rag.loader import load_markdown_documents
from app.rag.qdrant_store import QdrantStore, QdrantStoreError
from app.rag.splitter import split_markdown_documents
from app.rag.vectorstore import InMemoryVectorStore
from app.utils.config import get_config


class KnowledgeRetriever:
    def __init__(self) -> None:
        self.config = get_config()
        self.last_mode = "retrieval"
        self.last_error: str | None = None

    @cached_property
    def _keyword_store(self) -> InMemoryVectorStore:
        documents = load_markdown_documents(
            [
                self.config.faq_md,
                self.config.selection_rules_md,
                self.config.email_templates_md,
            ]
        )
        chunks = split_markdown_documents(documents)
        return InMemoryVectorStore(chunks)

    @cached_property
    def _qdrant_store(self) -> QdrantStore:
        return QdrantStore(
            url=self.config.rag.qdrant_url,
            collection_name=self.config.rag.qdrant_collection,
            vector_size=self.config.rag.qdrant_vector_size,
            embedding_provider=HashingEmbeddingProvider(
                self.config.rag.qdrant_vector_size
            ),
            timeout_seconds=self.config.rag.qdrant_timeout_seconds,
        )

    def retrieve(self, query: str, top_k: int = 4) -> list[dict[str, Any]]:
        if self.config.rag.use_qdrant:
            try:
                results = self._qdrant_store.search(query, top_k)
                if results:
                    self.last_mode = "qdrant"
                    self.last_error = None
                    return [result.to_dict() for result in results]
                self.last_error = "Qdrant returned no results; used keyword fallback."
            except QdrantStoreError as exc:
                self.last_error = f"{exc}; used keyword fallback."
            except Exception as exc:
                self.last_error = f"Unexpected Qdrant error: {exc}; used keyword fallback."
            self.last_mode = "keyword_fallback"
        else:
            self.last_mode = "retrieval"
            self.last_error = None

        results = self._keyword_store.similarity_search(query, top_k)
        return [result.to_dict() for result in results]
