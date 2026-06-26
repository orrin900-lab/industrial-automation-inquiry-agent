from app.schemas.product import ProductCandidate
from app.schemas.requirement import ExtractedRequirement


class ReplyGenerator:
    def generate_questions(
        self, requirement: ExtractedRequirement, missing_information: list[str]
    ) -> list[str]:
        if not missing_information:
            return [
                "Could you please confirm whether the extracted requirements are correct before our sales team prepares the next step?"
            ]

        questions: list[str] = []
        for item in missing_information:
            questions.append(self._question_for_item(requirement.product_category, item))
        return questions

    def generate_reply(
        self,
        requirement: ExtractedRequirement,
        missing_information: list[str],
        candidates: list[ProductCandidate],
        retrieved_context: list[dict[str, str]] | None = None,
    ) -> str:
        category = requirement.product_category or "the product"
        lines = [
            "Dear Customer,",
            "",
            "Thank you for your inquiry. Based on your message, we understand that you are looking for "
            f"{category} support for {requirement.application or 'your application'}.",
        ]

        if candidates:
            top = candidates[0]
            lines.append(
                "We found a preliminary candidate that may be relevant for technical review: "
                f"{top.product_name}. This is not a final model confirmation yet."
            )

        if missing_information:
            lines.append(
                "To help us confirm a suitable option, could you please provide the following information?"
            )
            for question in self.generate_questions(requirement, missing_information):
                lines.append(f"- {question}")
        else:
            lines.append(
                "The main technical information appears mostly complete. Our sales team can review it manually and confirm the next step."
            )

        lines.extend(
            [
                "",
                "Please note that price, stock status, and delivery time need to be checked and confirmed manually by our sales team after the exact model and quantity are confirmed.",
                "",
                "Best regards,",
                "Sales Support Team",
            ]
        )
        return "\n".join(lines)

    @staticmethod
    def _question_for_item(category: str | None, item: str) -> str:
        question_map = {
            "quantity": "Could you please confirm the required quantity?",
            "I/O points": "Could you please confirm the exact digital/analog input and output points?",
            "power_supply": "Could you please confirm the required power supply?",
            "communication": "Could you please confirm the required communication interface?",
            "output_type": "Could you please confirm whether relay output or transistor output is required?",
            "application": "Could you please share the application scenario or machine type?",
            "power_kw": "Could you please confirm the motor power in kW?",
            "input_voltage": "Could you please confirm the input voltage?",
            "phase": "Could you please confirm whether the input is single phase or three phase?",
            "screen_size": "Could you please confirm the preferred HMI screen size?",
            "protocol": "Could you please confirm the required communication protocol?",
            "port_count": "Could you please confirm the required port count?",
            "speed": "Could you please confirm whether 100M or Gigabit speed is required?",
            "poe_support": "Could you please confirm whether PoE is required?",
            "managed_type": "Could you please confirm whether managed or unmanaged type is required?",
            "product_category": "Could you please confirm the product category you need?",
        }
        return question_map.get(item, f"Could you please confirm {item}?")
