from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class InquiryInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    source: Literal["website", "email"] = Field(
        default="website",
        description="Inquiry entry source used by Agent Core.",
    )
    channel: Literal["website", "email"] | None = Field(
        default=None,
        description="A-stage API alias for source.",
    )
    message: str = Field(min_length=1, description="Raw inquiry message or email body.")
    subject: str | None = None
    name: str | None = None
    customer_name: str | None = None
    email: str | None = None
    customer_email: str | None = None
    from_email: str | None = None
    company: str | None = None
    country: str | None = None
    stated_product_category: str | None = None
    attachment_name: str | None = None
    attachments: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def normalize_api_aliases(self) -> "InquiryInput":
        if self.channel:
            self.source = self.channel
        else:
            self.channel = self.source

        if self.customer_name and not self.name:
            self.name = self.customer_name
        elif self.name and not self.customer_name:
            self.customer_name = self.name

        if self.customer_email and not self.email:
            self.email = self.customer_email
        elif self.email and not self.customer_email:
            self.customer_email = self.email

        if self.source == "email" and self.email and not self.from_email:
            self.from_email = self.email

        return self


class PublicInquiryInput(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=3)
    company: str | None = None
    country: str | None = None
    product_category: str | None = None
    message: str = Field(min_length=1)

    def to_inquiry_input(self) -> InquiryInput:
        subject = (
            f"{self.product_category} website inquiry"
            if self.product_category
            else "Website inquiry"
        )
        return InquiryInput(
            source="website",
            channel="website",
            customer_name=self.name,
            customer_email=self.email,
            company=self.company,
            country=self.country,
            subject=subject,
            stated_product_category=self.product_category,
            message=self.message,
            attachments=[],
        )


class InquiryStatusUpdate(BaseModel):
    status: str = Field(min_length=1)
