__all__ = [
    "MissingInfoChecker",
    "ProductMatcher",
    "RequirementExtractor",
    "ReplyGenerator",
    "RiskChecker",
    "export_agent_result_json",
    "export_demo_report_markdown",
]


def __getattr__(name: str):
    if name == "MissingInfoChecker":
        from app.services.missing_info_checker import MissingInfoChecker

        return MissingInfoChecker
    if name == "ProductMatcher":
        from app.services.product_matcher import ProductMatcher

        return ProductMatcher
    if name == "RequirementExtractor":
        from app.services.requirement_extractor import RequirementExtractor

        return RequirementExtractor
    if name == "ReplyGenerator":
        from app.services.reply_generator import ReplyGenerator

        return ReplyGenerator
    if name == "RiskChecker":
        from app.services.risk_checker import RiskChecker

        return RiskChecker
    if name == "export_agent_result_json":
        from app.services.exporter import export_agent_result_json

        return export_agent_result_json
    if name == "export_demo_report_markdown":
        from app.services.exporter import export_demo_report_markdown

        return export_demo_report_markdown
    raise AttributeError(name)
