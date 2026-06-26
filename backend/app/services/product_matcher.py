from app.data_access.product_repository import (
    ProductRepository,
    important_tokens,
    normalize_category,
    normalize_token,
    product_to_search_text,
)
from app.schemas.product import Product, ProductCandidate
from app.schemas.requirement import ExtractedRequirement


class ProductMatcher:
    def __init__(self, product_repository: ProductRepository | None = None) -> None:
        self.product_repository = product_repository or ProductRepository()

    def match(
        self, requirement: ExtractedRequirement, limit: int = 5
    ) -> list[ProductCandidate]:
        products = self.product_repository.list_products(requirement.product_category)
        candidates = [self._score_product(product, requirement) for product in products]
        candidates = [candidate for candidate in candidates if candidate.match_score > 0]
        candidates.sort(key=lambda candidate: candidate.match_score, reverse=True)
        return candidates[:limit]

    def _score_product(
        self, product: Product, requirement: ExtractedRequirement
    ) -> ProductCandidate:
        score = 0.0
        reason_parts: list[str] = []
        product_text = product_to_search_text(product)
        category = normalize_category(requirement.product_category)

        if (
            category
            and category != "Unknown"
            and normalize_category(product.category) == category
        ):
            score += 0.25
            reason_parts.append(f"Category matches {category}.")

        for key, value in requirement.technical_specs.items():
            if not value:
                continue
            value_text = str(value)
            normalized_value = normalize_token(value_text)
            product_value = getattr(product, key, None)
            if product_value and normalize_token(str(product_value)) == normalized_value:
                score += 0.12
                reason_parts.append(f"{key} matches {value_text}.")
            elif normalized_value and normalized_value in normalize_token(product_text):
                score += 0.07
                reason_parts.append(f"Product data contains {value_text}.")

        if requirement.application:
            tokens = important_tokens(requirement.application)
            matched_tokens = [token for token in tokens if token in product_text]
            if matched_tokens:
                score += min(0.15, 0.04 * len(matched_tokens))
                reason_parts.append("Application keywords overlap.")

        if requirement.brand and requirement.brand.lower() in product_text:
            score += 0.04
            reason_parts.append("Brand keyword appears in product data.")

        if requirement.model and normalize_token(requirement.model) in normalize_token(
            product_text
        ):
            score += 0.08
            reason_parts.append("Model or series keyword appears in product data.")

        keyword_overlap = self._keyword_overlap(product.match_keywords or "", requirement)
        if keyword_overlap:
            score += min(0.12, 0.03 * len(keyword_overlap))
            reason_parts.append(
                "Keyword overlap: " + ", ".join(keyword_overlap[:4]) + "."
            )

        if not reason_parts:
            reason_parts.append("Broad category fallback match; manual review required.")

        return ProductCandidate(
            product_id=product.product_id,
            product_name=product.product_name,
            category=product.category,
            match_score=min(round(score, 2), 1.0),
            match_reason=" ".join(reason_parts),
            missing_confirmations=self._candidate_missing_confirmations(requirement),
            product=product,
        )

    @staticmethod
    def _keyword_overlap(
        product_keywords: str, requirement: ExtractedRequirement
    ) -> list[str]:
        requirement_text = " ".join(
            [
                requirement.product_category or "",
                requirement.brand or "",
                requirement.model or "",
                requirement.application or "",
                " ".join(str(value) for value in requirement.technical_specs.values()),
            ]
        ).lower()
        keywords = [
            keyword.strip().lower()
            for keyword in product_keywords.replace(",", ";").split(";")
            if keyword.strip()
        ]
        return [keyword for keyword in keywords if keyword in requirement_text]

    @staticmethod
    def _candidate_missing_confirmations(requirement: ExtractedRequirement) -> list[str]:
        category = requirement.product_category
        specs = requirement.technical_specs
        if category == "PLC" and not specs.get("output_type"):
            return ["Confirm relay output or transistor output."]
        if category == "VFD" and not specs.get("motor_type"):
            return ["Confirm motor type before quotation."]
        if category == "HMI" and not specs.get("plc_compatibility"):
            return ["Confirm PLC brand/model compatibility."]
        if category == "Industrial Switch" and not specs.get("power_input"):
            return ["Confirm cabinet power input and working temperature."]
        return []
