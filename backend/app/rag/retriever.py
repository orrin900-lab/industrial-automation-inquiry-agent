from functools import cached_property
from typing import Any

from app.rag.loader import load_markdown_documents
from app.rag.splitter import split_markdown_documents
from app.rag.vectorstore import InMemoryVectorStore
from app.utils.config import get_config


class KnowledgeRetriever:
    def __init__(self) -> None:
        self.config = get_config()

    @cached_property
    def _store(self) -> InMemoryVectorStore:
        documents = load_markdown_documents(
            [
                self.config.faq_md,
                self.config.selection_rules_md,
                self.config.email_templates_md,
            ]
        )
        chunks = split_markdown_documents(documents)
        return InMemoryVectorStore(chunks)

    def retrieve(self, query: str, top_k: int = 4) -> list[dict[str, Any]]:
        results = self._store.similarity_search(query, top_k)
        return [result.to_dict() for result in results]
