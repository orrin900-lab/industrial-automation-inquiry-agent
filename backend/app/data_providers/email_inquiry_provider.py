from typing import Any

from app.data_providers.inquiry_source_provider import InquirySourceProvider
from app.schemas.inquiry import InquiryInput


class EmailInquiryProvider(InquirySourceProvider):
    provider_name = "email"

    def normalize(self, raw_input: InquiryInput | dict[str, Any]) -> InquiryInput:
        if isinstance(raw_input, InquiryInput):
            data = raw_input.model_dump()
        else:
            data = dict(raw_input)
        data["source"] = "email"
        data["channel"] = "email"
        return InquiryInput(**data)

