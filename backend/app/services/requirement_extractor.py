import re

from pydantic import BaseModel, Field, ValidationError

from app.agents.prompts import REQUIREMENT_EXTRACTION_PROMPT, SYSTEM_GUARDRAILS
from app.data_access.product_repository import normalize_category
from app.schemas.inquiry import InquiryInput
from app.schemas.requirement import ExtractedRequirement
from app.services.llm_client import LLMClient


class RequirementExtractionOutput(BaseModel):
    requirement: ExtractedRequirement
    missing_fields: list[str] = Field(default_factory=list)
    used_llm: bool = False
    mode: str = "fallback"
    error_message: str | None = None


class LLMRequirementPayload(BaseModel):
    product_category: str | None = None
    brand: str | None = None
    model: str | None = None
    quantity: str | None = None
    technical_specs: dict[str, str | int | float | bool | None] = Field(
        default_factory=dict
    )
    application: str | None = None
    destination_country: str | None = None
    missing_fields: list[str] = Field(default_factory=list)


class RequirementExtractor:
    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client or LLMClient()

    def extract(
        self,
        text: str,
        *,
        inquiry_input: InquiryInput,
        product_category: str | None = None,
    ) -> RequirementExtractionOutput:
        llm_output = self._extract_with_llm(
            text=text, inquiry_input=inquiry_input, product_category=product_category
        )
        if llm_output:
            return llm_output
        output = self.extract_with_rules(
            text=text, inquiry_input=inquiry_input, product_category=product_category
        )
        if self.llm_client.is_available():
            output.error_message = "LLM extraction returned invalid or empty JSON; used rule fallback."
        else:
            output.error_message = "LLM extraction disabled or API key missing; used rule fallback."
        return output

    def _extract_with_llm(
        self,
        *,
        text: str,
        inquiry_input: InquiryInput,
        product_category: str | None,
    ) -> RequirementExtractionOutput | None:
        if not self.llm_client.is_available():
            return None

        user_prompt = (
            f"Initial product category hint: {product_category or 'Unknown'}\n"
            f"Customer country: {inquiry_input.country or 'Unknown'}\n"
            f"Customer company: {inquiry_input.company or 'Unknown'}\n"
            f"Inquiry text:\n{text}"
        )
        data = self.llm_client.complete_json(
            SYSTEM_GUARDRAILS,
            REQUIREMENT_EXTRACTION_PROMPT + "\n\n" + user_prompt,
            response_name="requirement_extraction",
        )
        if not data:
            return None

        try:
            payload = LLMRequirementPayload.model_validate(data)
        except ValidationError:
            return None

        normalized_category = normalize_category(payload.product_category)
        if not normalized_category or normalized_category == "Unknown":
            normalized_category = normalize_category(product_category) or "Unknown"

        specs = {
            key: str(value)
            for key, value in payload.technical_specs.items()
            if value not in (None, "")
        }
        requirement = ExtractedRequirement(
            brand=payload.brand,
            model=payload.model,
            quantity=payload.quantity,
            product_category=normalized_category,
            technical_specs=specs,
            application=payload.application,
            destination_country=payload.destination_country or inquiry_input.country,
            customer_company=inquiry_input.company,
            customer_contact=inquiry_input.email or inquiry_input.from_email,
        )
        return RequirementExtractionOutput(
            requirement=requirement,
            missing_fields=payload.missing_fields,
            used_llm=True,
            mode="llm",
        )

    def extract_with_rules(
        self,
        *,
        text: str,
        inquiry_input: InquiryInput,
        product_category: str | None = None,
    ) -> RequirementExtractionOutput:
        normalized_category = normalize_category(product_category) or "Unknown"
        specs: dict[str, str] = {}

        for key, pattern in {
            "digital_inputs": r"(\d+)\s*(?:di|digital inputs?)\b",
            "digital_outputs": r"(\d+)\s*(?:do|digital outputs?)\b",
            "analog_inputs": r"(\d+)\s*(?:ai|analog inputs?)\b",
            "analog_outputs": r"(\d+)\s*(?:ao|analog outputs?)\b",
            "power_kw": r"(\d+(?:\.\d+)?)\s*kw\b",
            "screen_size": r"(\d+(?:\.\d+)?)\s*(?:inch|in)\b",
            "port_count": r"(\d+)[-\s]*(?:rj45\s*)?ports?\b",
            "fiber_ports": r"(\d+)\s*fiber ports?\b",
        }.items():
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                specs[key] = match.group(1)

        power_value = _find_first(
            text, r"\b(12-48V\s*DC|24V\s*DC|220V\s*AC|380V\s*AC)\b"
        )
        if power_value and normalized_category == "Industrial Switch":
            specs["power_input"] = power_value.upper().replace("  ", " ")
        elif power_value:
            specs["power_supply"] = power_value.upper().replace("  ", " ")

        input_voltage = _find_first(text, r"\b(220V|380V|400V|480V)\b")
        if input_voltage:
            specs["input_voltage"] = input_voltage.upper()

        if re.search(r"\bthree[-\s]?phase\b", text, re.IGNORECASE):
            specs["phase"] = "three phase"
        elif re.search(r"\bsingle[-\s]?phase\b", text, re.IGNORECASE):
            specs["phase"] = "single phase"

        communication = _find_terms(
            text, ["RS485", "RS232", "Ethernet", "CAN", "Profinet"]
        )
        if communication:
            specs["communication"] = ", ".join(communication)

        protocol = _find_terms(
            text, ["Modbus RTU", "Modbus TCP", "CANopen", "EtherNet/IP"]
        )
        if protocol:
            specs["protocol"] = ", ".join(protocol)

        if re.search(r"\brelay\b", text, re.IGNORECASE):
            specs["output_type"] = "relay"
        elif re.search(r"\btransistor\b", text, re.IGNORECASE):
            specs["output_type"] = "transistor"

        if re.search(r"\bgigabit\b", text, re.IGNORECASE):
            specs["speed"] = "Gigabit"
        elif re.search(r"\b100m\b|\bfast ethernet\b", text, re.IGNORECASE):
            specs["speed"] = "100M"

        if re.search(r"\bpoe\b", text, re.IGNORECASE):
            specs["poe_support"] = "true"
        if re.search(r"\bunmanaged\b", text, re.IGNORECASE):
            specs["managed_type"] = "unmanaged"
        elif re.search(r"\bmanaged\b", text, re.IGNORECASE):
            specs["managed_type"] = "managed"

        if re.search(r"\bwide temperature\b", text, re.IGNORECASE):
            specs["temperature_range"] = "wide temperature"

        resolution = _find_first(text, r"\b(\d{3,4}\s*x\s*\d{3,4})\b")
        if resolution:
            specs["resolution"] = resolution.replace(" ", "")

        if re.search(r"\bresistive\b", text, re.IGNORECASE):
            specs["touch_type"] = "resistive"
        elif re.search(r"\bcapacitive\b", text, re.IGNORECASE):
            specs["touch_type"] = "capacitive"

        if re.search(r"\bac motor\b", text, re.IGNORECASE):
            specs["motor_type"] = "AC motor"

        requirement = ExtractedRequirement(
            brand=_find_brand(text),
            model=_find_model(text),
            quantity=_find_quantity(text),
            product_category=normalized_category,
            technical_specs=specs,
            application=_find_application(text),
            destination_country=inquiry_input.country,
            customer_company=inquiry_input.company,
            customer_contact=inquiry_input.email or inquiry_input.from_email,
        )
        return RequirementExtractionOutput(
            requirement=requirement,
            used_llm=False,
            mode="fallback",
        )


def _find_quantity(text: str) -> str | None:
    match = re.search(
        r"(?:quantity\s*(?:is|:|may be)?\s*)?(\d+)\s*(pcs|pieces|units|sets)\b",
        text,
        flags=re.IGNORECASE,
    )
    if match:
        return f"{match.group(1)} {match.group(2).lower()}"
    return None


def _find_brand(text: str) -> str | None:
    brand_patterns = [
        r"\b(Siemens compatible)\b",
        r"\b(Mitsubishi(?:\s+FX)?(?:\s+series)?)\b",
        r"\b(ABB)\b",
        r"\b(Schneider)\b",
        r"\b(Omron)\b",
        r"\b(Allen[-\s]?Bradley)\b",
    ]
    for pattern in brand_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def _find_model(text: str) -> str | None:
    match = re.search(
        r"\b(?:model|series|alternative to|replacement for)\s+([A-Z0-9][A-Z0-9\-]{2,})\b",
        text,
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else None


def _find_application(text: str) -> str | None:
    patterns = [
        r"\bfor (?:a |an |the )?([a-z0-9 \-/]+?)(?:\.|,| with | required| need| please|$)",
        r"\bapplication is ([a-z0-9 \-/]+?)(?:\.|,| with | required| need| please|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _find_first(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else None


def _find_terms(text: str, terms: list[str]) -> list[str]:
    found: list[str] = []
    for term in terms:
        if re.search(rf"\b{re.escape(term)}\b", text, flags=re.IGNORECASE):
            found.append(term)
    return found
