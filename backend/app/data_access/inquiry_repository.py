import json
from pathlib import Path
from typing import Any

from app.utils.config import get_config


class InquiryRepository:
    def __init__(self, file_path: Path | None = None) -> None:
        self.file_path = file_path or get_config().sample_inquiries_json

    def list_sample_inquiries(self) -> list[dict[str, Any]]:
        if not self.file_path.exists():
            return []
        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
