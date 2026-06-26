from pydantic import BaseModel, Field


class Product(BaseModel):
    product_id: str
    product_name: str
    category: str
    brand: str | None = None
    series: str | None = None
    model: str | None = None
    digital_inputs: str | None = None
    digital_outputs: str | None = None
    analog_inputs: str | None = None
    analog_outputs: str | None = None
    output_type: str | None = None
    power_supply: str | None = None
    communication: str | None = None
    protocol: str | None = None
    power_kw: str | None = None
    input_voltage: str | None = None
    output_voltage: str | None = None
    phase: str | None = None
    control_mode: str | None = None
    motor_type: str | None = None
    screen_size: str | None = None
    resolution: str | None = None
    touch_type: str | None = None
    port_count: str | None = None
    port_type: str | None = None
    speed: str | None = None
    poe_support: str | None = None
    managed_type: str | None = None
    fiber_ports: str | None = None
    temperature_range: str | None = None
    application: str | None = None
    match_keywords: str | None = None


class ProductCandidate(BaseModel):
    product_id: str
    product_name: str
    category: str
    match_score: float = Field(ge=0.0, le=1.0)
    match_reason: str
    missing_confirmations: list[str] = Field(default_factory=list)
    product: Product | None = None
