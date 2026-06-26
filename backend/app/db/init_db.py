import os
import time

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
            return
        except SQLAlchemyError as exc:
            last_error = exc
            if attempt >= max_attempts:
                break
            time.sleep(retry_delay_seconds)

    raise RuntimeError(f"Database initialization failed: {last_error}") from last_error
