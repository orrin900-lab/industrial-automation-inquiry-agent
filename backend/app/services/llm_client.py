import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.utils.config import LLMConfig, get_config
from app.utils.logger import get_logger


class LLMClient:
    """Small optional LLM adapter.

    The C+ prototype must run without an API key, so all public methods return
    None on disabled config, HTTP errors, or invalid JSON.
    """

    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or get_config().llm
        self.logger = get_logger(__name__)

    def is_available(self) -> bool:
        return self.config.is_enabled

    def complete_json(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        response_name: str = "json_object",
    ) -> dict[str, Any] | None:
        if not self.is_available():
            return None
        if self.config.provider.lower() != "openai":
            self.logger.warning("Unsupported LLM provider: %s", self.config.provider)
            return None

        payload = {
            "model": self.config.openai_model,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        request = Request(
            f"{self.config.openai_base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.config.openai_api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.config.request_timeout_seconds) as resp:
                raw_body = resp.read().decode("utf-8")
            body = json.loads(raw_body)
            content = body["choices"][0]["message"]["content"]
            parsed = json.loads(content)
        except (HTTPError, URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError) as exc:
            self.logger.warning("LLM %s failed, falling back: %s", response_name, exc)
            return None

        return parsed if isinstance(parsed, dict) else None
