from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.utils.config import get_config


def _connect_args(database_url: str) -> dict:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


def _ensure_sqlite_directory(database_url: str) -> None:
    if not database_url.startswith("sqlite:///"):
        return
    path_text = database_url.replace("sqlite:///", "", 1)
    if path_text in {":memory:", ""}:
        return
    Path(path_text).parent.mkdir(parents=True, exist_ok=True)


config = get_config()
_ensure_sqlite_directory(config.database_url)
engine = create_engine(
    config.database_url,
    connect_args=_connect_args(config.database_url),
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
