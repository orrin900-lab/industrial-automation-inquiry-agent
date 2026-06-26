from app.data_access.product_repository import ProductRepository
from app.schemas.product import ProductCandidate


class RiskChecker:
    FORBIDDEN_PATTERNS = {
        "price promise": [
            "price is",
            "final price",
            "unit price",
            "we can quote usd",
            "quotation is",
            "we offer usd",
        ],
        "stock promise": [
            "in stock",
            "available from stock",
            "stock is ready",
            "ready stock",
        ],
        "lead time promise": [
            "delivery in",
            "lead time is",
            "ship within",
            "can deliver within",
        ],
        "certification or authorization promise": [
            "officially certified",
            "authorized distributor",
            "official siemens",
            "guaranteed compatible",
            "100% compatible",
        ],
    }

    OVER_CERTAIN_PATTERNS = [
        "the best model is",
        "the exact model is",
        "we confirm this model",
        "definitely suitable",
        "fully confirmed",
    ]

    def __init__(self, product_repository: ProductRepository | None = None) -> None:
        self.product_repository = product_repository or ProductRepository()

    def check(
        self,
        reply_draft: str,
        missing_information: list[str],
        candidates: list[ProductCandidate],
    ) -> list[str]:
        text = reply_draft.lower()
        flags = [
            "Manual review required before sending any reply.",
            "Do not quote price, promise stock, or promise delivery time in the prototype.",
            "Do not claim official brand compatibility without verification.",
        ]

        for label, patterns in self.FORBIDDEN_PATTERNS.items():
            if any(pattern in text for pattern in patterns):
                flags.append(f"Potential {label} detected in reply draft.")

        if missing_information:
            flags.append(
                "Missing key information remains: " + ", ".join(missing_information)
            )
            if any(pattern in text for pattern in self.OVER_CERTAIN_PATTERNS):
                flags.append(
                    "Avoid over-certain wording before key parameters are confirmed."
                )

        invalid_products = self._find_invalid_candidate_ids(candidates)
        if invalid_products:
            flags.append(
                "Recommended product is not present in products.csv: "
                + ", ".join(invalid_products)
            )

        if len(candidates) == 1 and missing_information:
            flags.append(
                "Avoid presenting a single candidate as final before missing information is confirmed."
            )

        return flags

    def _find_invalid_candidate_ids(
        self, candidates: list[ProductCandidate]
    ) -> list[str]:
        valid_ids = {
            product.product_id for product in self.product_repository.list_products()
        }
        return [
            candidate.product_id
            for candidate in candidates
            if candidate.product_id not in valid_ids
        ]
