from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class KnowledgeMetadata(BaseModel):
    source_file: str
    section_title: str
    chunk_id: str
    document_type: str


class KnowledgeDocument(BaseModel):
    source_file: str
    document_type: str
    content: str


class KnowledgeChunk(BaseModel):
    content: str
    metadata: KnowledgeMetadata


class RetrievedKnowledge(BaseModel):
    content: str
    score: float = Field(ge=0.0)
    metadata: KnowledgeMetadata

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def load_markdown_documents(paths: list[Path]) -> list[KnowledgeDocument]:
    documents: list[KnowledgeDocument] = []
    for path in paths:
        if not path.exists():
            continue
        documents.append(
            KnowledgeDocument(
                source_file=path.name,
                document_type=_document_type(path.name),
                content=path.read_text(encoding="utf-8"),
            )
        )
    return documents


def _document_type(file_name: str) -> str:
    name = file_name.lower()
    if "faq" in name:
        return "faq"
    if "selection" in name or "rule" in name:
        return "selection_rules"
    if "template" in name:
        return "email_templates"
    return "markdown"
