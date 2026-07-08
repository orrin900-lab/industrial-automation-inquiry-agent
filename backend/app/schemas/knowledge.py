from __future__ import annotations

from pydantic import BaseModel, Field


class KnowledgeStatusResponse(BaseModel):
    rag_mode: str
    qdrant_enabled: bool
    qdrant_available: bool
    collection_name: str
    points_count: int | None = None
    vector_size: int
    indexed_chunks: int
    source_files: list[str]
    fallback_available: bool = True
    embedding_provider: str = "deterministic_hashing"
    last_checked_at: str
    error_message: str | None = None


class KnowledgeChunkItem(BaseModel):
    chunk_id: str
    source_file: str
    section_title: str
    document_type: str
    content_preview: str
    content: str | None = None
    score: float | None = None


class KnowledgeChunksResponse(BaseModel):
    status: str = "success"
    items: list[KnowledgeChunkItem] = Field(default_factory=list)
    total: int = 0
    limit: int = 20
    offset: int = 0
    source_file: str | None = None
    error_message: str | None = None


class KnowledgeReindexResponse(BaseModel):
    success: bool
    collection_name: str
    indexed_chunks: int = 0
    points_count: int | None = None
    message: str
    error_message: str | None = None

