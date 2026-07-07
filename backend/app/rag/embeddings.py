from __future__ import annotations

import hashlib
import math
import re


class EmbeddingProvider:
    """Interface for replaceable embedding providers."""

    def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]


class HashingEmbeddingProvider(EmbeddingProvider):
    """Deterministic local embedding for prototype vector retrieval.

    This avoids external API keys and model downloads while keeping the
    retriever interface close to production vector search.
    """

    def __init__(self, vector_size: int = 384) -> None:
        if vector_size <= 0:
            raise ValueError("vector_size must be greater than 0.")
        self.vector_size = vector_size

    def embed_text(self, text: str) -> list[float]:
        vector = [0.0] * self.vector_size
        tokens = _tokenize(text)
        if not tokens:
            return vector

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.vector_size
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [round(value / norm, 6) for value in vector]


def _tokenize(text: str) -> list[str]:
    normalized = text.lower()
    return re.findall(r"[\w]+", normalized, flags=re.UNICODE)
