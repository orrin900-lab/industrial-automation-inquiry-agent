from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel


class LLMConfig(BaseModel):
    provider: str = "openai"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"
    enable_llm_extraction: bool = False
    request_timeout_seconds: int = 30

    @property
    def is_enabled(self) -> bool:
        return (
            self.enable_llm_extraction
            and self.provider.lower() == "openai"
            and bool(self.openai_api_key)
        )


class RAGConfig(BaseModel):
    enable_qdrant_rag: bool = False
    qdrant_url: str = "http://127.0.0.1:6333"
    qdrant_collection: str = "industrial_agent_knowledge"
    qdrant_vector_size: int = 384
    qdrant_timeout_seconds: float = 3.0
    rag_retrieval_mode: str = "keyword"

    @property
    def use_qdrant(self) -> bool:
        return (
            self.enable_qdrant_rag
            and self.rag_retrieval_mode.strip().lower() == "qdrant"
        )


class AppConfig(BaseModel):
    project_root: Path
    data_dir: Path
    products_csv: Path
    sample_inquiries_json: Path
    faq_md: Path
    selection_rules_md: Path
    email_templates_md: Path
    storage_dir: Path
    database_url: str
    llm: LLMConfig
    rag: RAGConfig


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")
    data_dir = project_root / "data"
    storage_dir = project_root / "storage"
    return AppConfig(
        project_root=project_root,
        data_dir=data_dir,
        products_csv=data_dir / "products.csv",
        sample_inquiries_json=data_dir / "sample_inquiries.json",
        faq_md=data_dir / "faq.md",
        selection_rules_md=data_dir / "selection_rules.md",
        email_templates_md=data_dir / "email_templates.md",
        storage_dir=storage_dir,
        database_url=os.getenv("DATABASE_URL", "sqlite:///./storage/dev.db"),
        llm=LLMConfig(
            provider=os.getenv("LLM_PROVIDER", "openai"),
            openai_api_key=os.getenv("OPENAI_API_KEY") or None,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            openai_base_url=os.getenv(
                "OPENAI_BASE_URL", "https://api.openai.com/v1"
            ).rstrip("/"),
            enable_llm_extraction=_to_bool(os.getenv("ENABLE_LLM_EXTRACTION", "false")),
            request_timeout_seconds=int(os.getenv("LLM_REQUEST_TIMEOUT_SECONDS", "30")),
        ),
        rag=RAGConfig(
            enable_qdrant_rag=_to_bool(os.getenv("ENABLE_QDRANT_RAG", "false")),
            qdrant_url=os.getenv("QDRANT_URL", "http://127.0.0.1:6333").rstrip("/"),
            qdrant_collection=os.getenv(
                "QDRANT_COLLECTION", "industrial_agent_knowledge"
            ),
            qdrant_vector_size=int(os.getenv("QDRANT_VECTOR_SIZE", "384")),
            qdrant_timeout_seconds=float(os.getenv("QDRANT_TIMEOUT_SECONDS", "3")),
            rag_retrieval_mode=os.getenv("RAG_RETRIEVAL_MODE", "keyword"),
        ),
    )


def _to_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}
