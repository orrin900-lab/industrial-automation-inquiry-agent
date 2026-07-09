from app.data_providers import (
    EmailInquiryProvider,
    ManualInquiryProvider,
    WebsiteInquiryProvider,
    get_inquiry_source_provider,
)
from app.schemas.inquiry import InquiryInput
from app.utils.config import get_config


def test_manual_inquiry_provider_normalizes_raw_dict():
    provider = ManualInquiryProvider()

    inquiry = provider.normalize(
        {
            "channel": "website",
            "customer_name": "John Smith",
            "customer_email": "john@example.com",
            "message": "Need PLC with 16DI and 8DO.",
        }
    )

    assert isinstance(inquiry, InquiryInput)
    assert inquiry.source == "website"
    assert inquiry.customer_name == "John Smith"
    assert inquiry.email == "john@example.com"


def test_website_and_email_providers_set_source():
    website = WebsiteInquiryProvider().normalize(
        {"message": "Need HMI for packaging line."}
    )
    email = EmailInquiryProvider().normalize(
        {"message": "Need VFD for pump.", "email": "buyer@example.com"}
    )

    assert website.source == "website"
    assert website.channel == "website"
    assert email.source == "email"
    assert email.channel == "email"
    assert email.from_email == "buyer@example.com"


def test_unknown_inquiry_source_provider_falls_back_to_manual(monkeypatch):
    monkeypatch.setenv("INQUIRY_SOURCE_PROVIDER", "crm")
    get_config.cache_clear()

    provider = get_inquiry_source_provider()

    assert isinstance(provider, ManualInquiryProvider)
    assert provider.fallback_reason
    assert "falling back" in provider.fallback_reason

