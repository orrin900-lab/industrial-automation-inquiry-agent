# Project Summary

## Project Positioning

Industrial Automation Inquiry Agent is a full-stack AI Agent prototype for B2B export sales teams. It focuses on technical inquiry qualification rather than autonomous sales. The project demonstrates how Agent workflows, structured outputs, RAG, persistence, observability, and human review can work together in a practical business scenario.

## Completed Capabilities

- FastAPI backend for Agent Core APIs.
- Next.js frontend sales console.
- PostgreSQL persistence through Docker Compose.
- SQLite fallback for local backend development.
- Rule fallback plus optional LLM JSON extraction.
- Lightweight RAG over Markdown knowledge files.
- Product repository and candidate matching.
- Structured AgentResult schema.
- Agent Execution Trace.
- Retrieved Knowledge Sources.
- Human review form and review logs.
- Docker Compose one-command startup.
- Real screenshots for dashboard, analyze form, AgentResult, inquiry list/detail, candidate products, RAG sources, Agent Trace, review form, and Swagger.

## Current Tech Stack

- Next.js
- TypeScript
- Tailwind CSS
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Docker Compose
- Lightweight RAG
- pytest

## Current Business Loop

1. Sales user submits inquiry.
2. Backend saves inquiry.
3. Agent Core analyzes inquiry.
4. Backend saves AgentResult and trace.
5. Frontend displays structured result.
6. Sales user edits English reply draft.
7. Sales user submits review status.
8. Review log is persisted.

## Engineering Maturity

The project has moved beyond a simple demo:

- API layer separated from business logic.
- Repository and retriever interfaces exist.
- Database persistence is implemented.
- Docker Compose can run the whole stack.
- Docker Compose has passed actual runtime validation with PostgreSQL, backend, and frontend services healthy.
- Frontend displays structured sections rather than raw JSON only.
- Agent Trace improves observability.
- README and docs now include portfolio-oriented architecture, API overview, demo script, resume description, interview guide, and real screenshots.

The project is currently suitable for GitHub, resume, interview, and short recording demonstrations.

## Current Limits

- Product data and inquiry data are high-fidelity simulated data.
- Lightweight RAG is not a production vector database.
- No authentication or role-based access control.
- No CRM, ERP, live inventory, quotation, or email integration.
- No Qdrant or Redis integration.
- No production deployment pipeline.
- No automatic pricing, stock, lead time, or email sending.

## Future Roadmap

- Record a short 3-5 minute demo video.
- Add Alembic migrations.
- Replace lightweight RAG with Qdrant.
- Add Redis for async jobs.
- Add authentication and permissions.
- Add knowledge base management UI.
- Enhance email inquiry import.
- Add CRM/ERP/email integrations with approval gates.
- Add production observability and audit logs.
- Expand tests with more real-world inquiry cases.
