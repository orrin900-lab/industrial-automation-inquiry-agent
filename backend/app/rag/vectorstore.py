from collections import Counter

from app.rag.loader import KnowledgeChunk, RetrievedKnowledge


class InMemoryVectorStore:
    """A replaceable lexical store used until Chroma/Qdrant is introduced."""

    def __init__(self, chunks: list[KnowledgeChunk]) -> None:
        self.chunks = chunks

    def similarity_search(self, query: str, top_k: int = 4) -> list[RetrievedKnowledge]:
        query_terms = Counter(tokenize(query))
        if not query_terms:
            return [
                RetrievedKnowledge(content=chunk.content, score=0.0, metadata=chunk.metadata)
                for chunk in self.chunks[:top_k]
            ]

        scored: list[RetrievedKnowledge] = []
        for chunk in self.chunks:
            text = " ".join(
                [
                    chunk.content,
                    chunk.metadata.source_file,
                    chunk.metadata.section_title,
                    chunk.metadata.document_type,
                ]
            )
            doc_terms = Counter(tokenize(text))
            raw_score = sum(query_terms[token] * doc_terms[token] for token in query_terms)
            if raw_score <= 0:
                continue
            normalized = min(1.0, raw_score / max(sum(query_terms.values()), 1))
            scored.append(
                RetrievedKnowledge(
                    content=chunk.content,
                    score=round(float(normalized), 3),
                    metadata=chunk.metadata,
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]


def tokenize(text: str) -> list[str]:
    normalized = (
        text.lower()
        .replace("/", " ")
        .replace("-", " ")
        .replace("_", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace("?", " ")
        .replace(":", " ")
        .replace(";", " ")
    )
    return [token for token in normalized.split() if len(token) > 2]
