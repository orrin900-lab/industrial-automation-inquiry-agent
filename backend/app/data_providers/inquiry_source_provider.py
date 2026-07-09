from abc import ABC, abstractmethod
from typing import Any

from app.schemas.inquiry import InquiryInput
from app.utils.config import get_config


class InquirySourceProvider(ABC):
    provider_name: str
    fallback_reason: str | None = None

    @abstractmethod
    def normalize(self, raw_input: InquiryInput | dict[str, Any]) -> InquiryInput:
        raise NotImplementedError


def get_inquiry_source_provider(provider_name: str | None = None) -> InquirySourceProvider:
    from app.data_providers.email_inquiry_provider import EmailInquiryProvider
    from app.data_providers.manual_inquiry_provider import ManualInquiryProvider
    from app.data_providers.website_inquiry_provider import WebsiteInquiryProvider

    requested = (
        provider_name or get_config().data_providers.inquiry_source_provider
    ).strip().lower()
    if requested == "manual":
        return ManualInquiryProvider()
    if requested == "website":
        return WebsiteInquiryProvider()
    if requested == "email":
        return EmailInquiryProvider()

    fallback_reason = (
        f"INQUIRY_SOURCE_PROVIDER={requested!r} is unsupported in the prototype; "
        "falling back to ManualInquiryProvider."
    )
    return ManualInquiryProvider(fallback_reason=fallback_reason)

