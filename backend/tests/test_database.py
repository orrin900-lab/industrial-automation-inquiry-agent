from app.db.models import AgentResultRecord, AgentRun, AgentStep, Inquiry, ReviewLog
from app.db.session import engine


def test_database_tables_are_created():
    table_names = set(Inquiry.metadata.tables.keys())
    assert {
        "inquiries",
        "agent_results",
        "agent_runs",
        "agent_steps",
        "review_logs",
    }.issubset(table_names)

    assert engine.url.drivername == "sqlite"
    assert Inquiry.__tablename__ == "inquiries"
    assert AgentResultRecord.__tablename__ == "agent_results"
    assert AgentRun.__tablename__ == "agent_runs"
    assert AgentStep.__tablename__ == "agent_steps"
    assert ReviewLog.__tablename__ == "review_logs"
