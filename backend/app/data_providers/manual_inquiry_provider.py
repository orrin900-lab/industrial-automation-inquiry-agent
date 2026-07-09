from typing import Any

from app.data_providers.inquiry_source_provider import InquirySourceProvider
from app.schemas.inquiry import InquiryInput


class ManualInquiryProvider(InquirySourceProvider):
    provider_name = "manual"

    def __init__(self, *, fallback_reason: str | None = None) -> None:
        self.fallback_reason = fallback_reason

    def normalize(self, raw_input: InquiryInput | dict[str, Any]) -> InquiryInput:
        if isinstance(raw_input, InquiryInput):
            return raw_input
        return InquiryInput(**raw_input)

