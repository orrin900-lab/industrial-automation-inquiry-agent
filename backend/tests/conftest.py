import os
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./storage/test.db"
os.environ["ENABLE_LLM_EXTRACTION"] = "false"
os.environ.pop("OPENAI_API_KEY", None)

from app.db.base import Base
from app.db.session import engine


def pytest_runtest_setup(item):
    Path("storage").mkdir(exist_ok=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
