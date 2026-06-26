from pydantic import BaseModel, Field


class ExtractedRequirement(BaseModel):
    brand: str | None = None
    model: str | None = None
    quantity: str | None = None
    product_category: str | None = None
    technical_specs: dict[str, str] = Field(default_factory=dict)
    application: str | None = None
    destination_country: str | None = None
    customer_company: str | None = None
    customer_contact: str | None = None
