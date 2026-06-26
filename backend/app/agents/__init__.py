__all__ = ["run_inquiry_agent"]


def __getattr__(name: str):
    if name == "run_inquiry_agent":
        from app.agents.graph import run_inquiry_agent

        return run_inquiry_agent
    raise AttributeError(name)
