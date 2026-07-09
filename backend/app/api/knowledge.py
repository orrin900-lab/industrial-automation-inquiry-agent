from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import require_roles
from app.services.knowledge_service import (
    get_knowledge_status,
    list_knowledge_chunks,
    rebuild_knowledge_index,
    upload_knowledge_markdown,
)
from app.schemas.knowledge import KnowledgeUploadInput


router = APIRouter(
    prefix="/knowledge",
    tags=["knowledge"],
    dependencies=[Depends(require_roles("admin"))],
)


@router.get("/status")
def get_knowledge_status_endpoint() -> dict:
    return get_knowledge_status().model_dump(mode="json")


@router.get("/chunks")
def list_knowledge_chunks_endpoint(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    source_file: str | None = None,
) -> dict:
    return list_knowledge_chunks(
        limit=limit,
        offset=offset,
        source_file=source_file,
    ).model_dump(mode="json")


@router.post("/reindex")
def rebuild_knowledge_index_endpoint() -> dict:
    return rebuild_knowledge_index().model_dump(mode="json")


@router.post("/upload")
def upload_knowledge_markdown_endpoint(payload: KnowledgeUploadInput) -> dict:
    return upload_knowledge_markdown(payload).model_dump(mode="json")

