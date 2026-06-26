from app.schemas.requirement import ExtractedRequirement


class MissingInfoChecker:
    REQUIRED_FIELDS = {
        "PLC": [
            ("quantity", "quantity"),
            ("I/O points", ("digital_inputs", "digital_outputs")),
            ("power_supply", "power_supply"),
            ("communication", "communication"),
            ("output_type", "output_type"),
            ("application", "application"),
        ],
        "VFD": [
            ("power_kw", "power_kw"),
            ("input_voltage", "input_voltage"),
            ("phase", "phase"),
            ("application", "application"),
            ("quantity", "quantity"),
        ],
        "HMI": [
            ("screen_size", "screen_size"),
            ("communication", "communication"),
            ("protocol", "protocol"),
            ("quantity", "quantity"),
            ("application", "application"),
        ],
        "Industrial Switch": [
            ("port_count", "port_count"),
            ("speed", "speed"),
            ("poe_support", "poe_support"),
            ("managed_type", "managed_type"),
            ("quantity", "quantity"),
            ("application", "application"),
        ],
    }

    def check(self, requirement: ExtractedRequirement) -> list[str]:
        category = requirement.product_category or "Unknown"
        required = self.REQUIRED_FIELDS.get(category, [])
        missing: list[str] = []
        for label, key in required:
            if isinstance(key, tuple):
                if not all(self._has_value(requirement, item) for item in key):
                    missing.append(label)
            elif not self._has_value(requirement, key):
                missing.append(label)
        if category == "Unknown":
            missing.append("product_category")
        return missing

    @staticmethod
    def _has_value(requirement: ExtractedRequirement, key: str) -> bool:
        if key == "quantity":
            return bool(requirement.quantity)
        if key == "application":
            return bool(requirement.application)
        return bool(requirement.technical_specs.get(key))
