from app.rag.loader import KnowledgeMetadata, RetrievedKnowledge
from app.rag.retriever import KnowledgeRetriever
from app.utils.config import get_config


class FakeQdrantStore:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def search(self, query: str, top_k: int = 4) -> list[RetrievedKnowledge]:
        return [
            RetrievedKnowledge(
                content="Use PLC selection rules to confirm I/O count and communication.",
                score=0.91,
                metadata=KnowledgeMetadata(
                    source_file="selection_rules.md",
                    section_title="PLC Selection",
                    document_type="selection_rules",
                    chunk_id="selection_rules.md:1:1",
                ),
            )
        ][:top_k]


def test_retriever_uses_qdrant_when_available(monkeypatch):
    monkeypatch.setenv("ENABLE_QDRANT_RAG", "true")
    monkeypatch.setenv("RAG_RETRIEVAL_MODE", "qdrant")
    monkeypatch.setenv("QDRANT_URL", "http://qdrant:6333")
    get_config.cache_clear()
    monkeypatch.setattr("app.rag.retriever.QdrantStore", FakeQdrantStore)

    retriever = KnowledgeRetriever()
    results = retriever.retrieve("PLC communication selection", top_k=1)

    assert retriever.last_mode == "qdrant"
    assert results == [
        {
            "content": "Use PLC selection rules to confirm I/O count and communication.",
            "score": 0.91,
            "metadata": {
                "source_file": "selection_rules.md",
                "section_title": "PLC Selection",
                "document_type": "selection_rules",
                "chunk_id": "selection_rules.md:1:1",
            },
        }
    ]


def test_retriever_keyword_mode_structure(monkeypatch):
    monkeypatch.setenv("ENABLE_QDRANT_RAG", "false")
    monkeypatch.setenv("RAG_RETRIEVAL_MODE", "keyword")
    get_config.cache_clear()

    retriever = KnowledgeRetriever()
    results = retriever.retrieve("HMI screen Modbus", top_k=2)

    assert retriever.last_mode == "retrieval"
    assert results
    first = results[0]
    assert {"content", "score", "metadata"}.issubset(first.keys())
    assert {"source_file", "section_title", "document_type", "chunk_id"}.issubset(
        first["metadata"].keys()
    )
