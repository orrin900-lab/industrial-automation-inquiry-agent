import csv
from functools import cached_property
from pathlib import Path

from app.schemas.product import Product, ProductCandidate
from app.schemas.requirement import ExtractedRequirement
from app.utils.config import get_config


CATEGORY_ALIASES = {
    "plc": "PLC",
    "vfd": "VFD",
    "inverter": "VFD",
    "drive": "VFD",
    "hmi": "HMI",
    "touch panel": "HMI",
    "operator panel": "HMI",
    "industrial switch": "Industrial Switch",
    "switch": "Industrial Switch",
}


class ProductRepository:
    def __init__(self, csv_path: Path | None = None) -> None:
        self.csv_path = csv_path or get_config().products_csv

    @cached_property
    def _products(self) -> list[Product]:
        if not self.csv_path.exists():
            return []

        products: list[Product] = []
        with self.csv_path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cleaned = {key: self._clean(value) for key, value in row.items()}
                products.append(Product(**cleaned))
        return products

    def list_products(self, category: str | None = None) -> list[Product]:
        normalized_category = normalize_category(category)
        if not normalized_category or normalized_category == "Unknown":
            return list(self._products)
        return [
            product
            for product in self._products
            if normalize_category(product.category) == normalized_category
        ]

    def search_candidates(
        self, requirement: ExtractedRequirement, limit: int = 3
    ) -> list[ProductCandidate]:
        products = self.list_products(requirement.product_category)
        scored = [
            self._score_product(product, requirement)
            for product in products
        ]
        scored = [candidate for candidate in scored if candidate.match_score > 0]
        scored.sort(key=lambda candidate: candidate.match_score, reverse=True)
        return scored[:limit]

    def _score_product(
        self, product: Product, requirement: ExtractedRequirement
    ) -> ProductCandidate:
        score = 0.12
        reasons: list[str] = []
        category = normalize_category(requirement.product_category)
        product_text = product_to_search_text(product)
        specs = {
            key: value.lower()
            for key, value in requirement.technical_specs.items()
            if value
        }

        if category and category != "Unknown" and normalize_category(product.category) == category:
            score += 0.18
            reasons.append(f"category matches {category}")

        for field_name, field_value in specs.items():
            value = normalize_token(field_value)
            if not value:
                continue
            product_value = getattr(product, field_name, None)
            if product_value and normalize_token(str(product_value)) == value:
                score += 0.14
                reasons.append(f"{field_name} matches {field_value}")
            elif value in product_text:
                score += 0.08
                reasons.append(f"contains {field_value}")

        if requirement.application:
            app_tokens = important_tokens(requirement.application)
            matched = [token for token in app_tokens if token in product_text]
            if matched:
                score += min(0.16, 0.05 * len(matched))
                reasons.append("application keywords overlap")

        if requirement.model and requirement.model.lower() in product_text:
            score += 0.12
            reasons.append("model keyword appears in product data")

        if requirement.brand and requirement.brand.lower() in product_text:
            score += 0.04
            reasons.append("brand keyword appears in product data")

        score = min(round(score, 2), 0.95)
        if not reasons:
            reasons.append("same product family or broad keyword match only")

        return ProductCandidate(
            product_id=product.product_id,
            product_name=product.product_name,
            category=product.category,
            match_score=score,
            match_reason="; ".join(reasons),
            missing_confirmations=[],
            product=product,
        )

    @staticmethod
    def _clean(value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None


def normalize_category(category: str | None) -> str | None:
    if not category:
        return None
    text = category.strip().lower()
    if text in {"", "unknown", "not sure"}:
        return "Unknown"
    return CATEGORY_ALIASES.get(text, category.strip())


def product_to_search_text(product: Product) -> str:
    values = [
        str(value).lower()
        for value in product.model_dump(exclude_none=True).values()
    ]
    return " ".join(values).replace(";", " ")


def normalize_token(value: str | None) -> str:
    if not value:
        return ""
    return (
        value.lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
        .replace("/", "")
    )


def important_tokens(text: str) -> list[str]:
    stop_words = {
        "for",
        "with",
        "and",
        "the",
        "need",
        "needs",
        "required",
        "please",
        "machine",
        "application",
    }
    return [
        token
        for token in text.lower().replace("/", " ").replace("-", " ").split()
        if len(token) > 2 and token not in stop_words
    ]
