import os
import time

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from app.db.base import Base
from app.db.session import engine


def init_db() -> None:
    max_attempts = int(os.getenv("DB_INIT_MAX_ATTEMPTS", "10"))
    retry_delay_seconds = float(os.getenv("DB_INIT_RETRY_DELAY_SECONDS", "2"))
    last_error: SQLAlchemyError | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            from app.db import models  # noqa: F401

            Base.metadata.create_all(bind=engine)
            _ensure_lightweight_schema_upgrades()
            return
        except SQLAlchemyError as exc:
            last_error = exc
            if attempt >= max_attempts:
                break
            time.sleep(retry_delay_seconds)

    raise RuntimeError(f"Database initialization failed: {last_error}") from last_error


def _ensure_lightweight_schema_upgrades() -> None:
    """Small prototype migrations before Alembic is introduced."""
    inspector = inspect(engine)
    if "review_logs" not in inspector.get_table_names():
        return

    review_columns = {column["name"] for column in inspector.get_columns("review_logs")}
    if "reviewer_role" not in review_columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE review_logs ADD COLUMN reviewer_role VARCHAR(50)")
            )
