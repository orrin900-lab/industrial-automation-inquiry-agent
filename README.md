# Industrial Automation Inquiry Agent

An AI-assisted inquiry qualification platform for industrial automation export sales. The system helps customer service and sales users process website and email inquiries for PLC, VFD, HMI, and Industrial Switch products, extract structured requirements, retrieve product and knowledge references, recommend candidate products, draft an English reply, and record human review decisions.

This project is packaged as a portfolio-ready full-stack AI application: `Next.js + FastAPI + Agent Core + PostgreSQL + Docker Compose`.

## 1. Project Overview

Industrial Automation Inquiry Agent is designed for B2B export sales teams handling technical inquiries from overseas customers. Instead of acting as a fully autonomous sales bot, it works as an internal decision-support assistant. It converts messy inquiry text into a structured `AgentResult`, keeps an execution trace, and leaves the final reply to a human sales user.

Current deployment modes:

- Docker Compose one-command stack with PostgreSQL, FastAPI backend, and Next.js frontend.
- Local development mode with SQLite fallback for backend testing.

Related docs:

- [Architecture](docs/architecture.md)
- [Demo Script](docs/demo_script.md)
- [API Overview](docs/api_overview.md)
- [Interview Guide](docs/interview_guide.md)
- [Resume Description](docs/resume_description.md)
- [Project Summary](docs/project_summary.md)
- [Manual Test Report](docs/manual_test_report.md)

## 2. Business Scenario

Industrial automation export inquiries often contain incomplete technical details:

- "Need Siemens compatible PLC, 16DI and 8DO, RS485."
- "Looking for 2.2kW VFD for water pump, 380V three phase."
- "Need 7 inch HMI with Ethernet and Modbus TCP."
- "Looking for 8-port gigabit industrial switch, unmanaged is ok."

Sales users need to quickly understand the product category, missing parameters, matching candidates, and safe follow-up questions. This project supports that workflow while preserving manual review and business risk control.

## 3. Key Features

- Website Inquiry and Email Inquiry input flows.
- Sample inquiry loading for PLC, VFD, HMI, and Industrial Switch scenarios.
- Rule fallback plus optional LLM JSON extraction.
- Structured `AgentResult` output with Pydantic schemas.
- Requirement extraction: category, brand, model, quantity, technical specs, application, destination country.
- Missing information detection and clarification questions.
- Product matching from `products.csv`, with match score, reason, and missing confirmations.
- Lightweight RAG over Markdown knowledge files.
- Retrieved Knowledge Sources shown in frontend.
- Agent Execution Trace for observability.
- Risk flags for price, stock, delivery, compatibility, and certification claims.
- English reply draft generation for manual review.
- PostgreSQL persistence for inquiries, AgentResult, AgentRun, AgentStep, and ReviewLog.
- Human-in-the-loop review form.
- Docker Compose startup chain.

## 4. Architecture

```mermaid
flowchart TD
    U[Sales User / Operator] --> F[Next.js Frontend]
    F --> B[FastAPI Backend]
    B --> S[Agent Service]
    S --> A[Agent Core]
    A --> R[Lightweight RAG Retriever]
    A --> P[Product Repository]
    S --> DB[(PostgreSQL)]
    DB --> S
```

The frontend is a sales console. The backend exposes stable REST APIs. The Agent Core owns inquiry classification, extraction, retrieval, product matching, reply drafting, and risk checks. PostgreSQL stores the workflow records and review decisions.

See [docs/architecture.md](docs/architecture.md) for the detailed architecture and evolution path.

## 5. Tech Stack

- Frontend: Next.js, TypeScript, Tailwind CSS, App Router
- Backend: FastAPI, Pydantic, SQLAlchemy
- Database: PostgreSQL by Docker Compose, SQLite fallback for local development
- Agent Core: rule-based fallback, optional LLM JSON extraction, structured workflow nodes
- RAG: lightweight Markdown loader, splitter, keyword retriever
- Observability: Agent Execution Trace, retrieved source metadata
- DevOps: Docker Compose, Dockerfiles, healthchecks
- Testing: pytest, Next.js build/type checks

## 6. Agent Workflow

```mermaid
flowchart LR
    I[InquiryInput] --> C[Intent Classifier]
    C --> K[Product Category Classifier]
    K --> E[Requirement Extractor]
    E --> M[Missing Info Checker]
    M --> R[Knowledge Retriever]
    R --> P[Product Matcher]
    P --> D[Reply Draft Generator]
    D --> X[Risk Checker]
    X --> O[Structured AgentResult]
```

Each step writes trace information:

- `step_name`
- `mode`: rule, llm, fallback, retrieval, hybrid
- input and output summary
- success flag
- error message
- latency

If LLM extraction is disabled or unavailable, the workflow falls back to deterministic rules so the demo remains runnable.

## 7. Data Flow

```mermaid
sequenceDiagram
    participant User as Sales User
    participant UI as Next.js Frontend
    participant API as FastAPI Backend
    participant Agent as Agent Core
    participant DB as PostgreSQL

    User->>UI: Submit inquiry
    UI->>API: POST /api/inquiries/analyze
    API->>DB: Save inquiry
    API->>Agent: Run analysis
    Agent-->>API: AgentResult + trace + retrieved knowledge
    API->>DB: Save AgentResult, AgentRun, AgentStep
    API-->>UI: inquiry_id + agent_result
    User->>UI: Review reply draft
    UI->>API: POST /api/inquiries/{id}/review
    API->>DB: Save review log and status
```

## 8. Screenshots

Real screenshots are stored in [docs/screenshots](docs/screenshots). The Docker Compose terminal screenshot is still pending, but the frontend and Swagger screenshots below were captured from the running stack.

![Dashboard](docs/screenshots/01_dashboard.png)

![Analyze Form](docs/screenshots/02_analyze_form.png)

![Agent Result](docs/screenshots/03_agent_result.png)

![Inquiry Detail](docs/screenshots/05_inquiry_detail.png)

![Candidate Products](docs/screenshots/06_candidate_products.png)

![Retrieved Knowledge](docs/screenshots/07_retrieved_knowledge.png)

![Agent Trace](docs/screenshots/08_agent_trace.png)

![Review Form](docs/screenshots/09_review_form.png)

![Swagger API](docs/screenshots/10_swagger_api.png)

The full screenshot checklist and pending status are maintained in [docs/screenshots/README.md](docs/screenshots/README.md).

## 9. Quick Start with Docker Compose

From the project root:

```bash
docker-compose up --build
```

If your Docker CLI supports the newer syntax:

```bash
docker compose up --build
```

Access:

```text
Frontend: http://127.0.0.1:3001
Backend API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs
PostgreSQL: localhost:5432
```

Stop services:

```bash
docker-compose down
```

Clear database volume:

```bash
docker-compose down -v
```

Docker Compose uses PostgreSQL by default:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/industrial_agent
```

## 10. Local Development

Backend:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev -- -H 127.0.0.1 -p 3001
```

Backend tests:

```bash
cd backend
PYTHONPATH=. pytest
```

Frontend build:

```bash
cd frontend
npm run build
```

Local development keeps SQLite fallback unless `DATABASE_URL` is set.

## 11. API Overview

Main APIs:

- `GET /api/health`
- `POST /api/inquiries/analyze`
- `GET /api/inquiries`
- `GET /api/inquiries/{id}`
- `POST /api/inquiries/{id}/review`
- `GET /api/inquiries/samples`

Full API notes are available in [docs/api_overview.md](docs/api_overview.md).

## 12. Demo Workflow

Recommended demo flow:

1. Start Docker Compose.
2. Open `http://127.0.0.1:3001`.
3. Check backend health on dashboard.
4. Go to Analyze Inquiry.
5. Load a PLC sample.
6. Submit analysis.
7. Show AgentResult, candidate products, missing information, retrieved knowledge, and trace.
8. Open detail page.
9. Edit English reply draft.
10. Submit review.
11. Show inquiry list and PostgreSQL persistence.

Detailed narration is in [docs/demo_script.md](docs/demo_script.md).

## 13. Prototype Boundary

This is an engineering prototype and portfolio project, not a production sales automation system.

Important boundaries:

- Current product data is high-fidelity simulated data.
- Lightweight RAG is not a final production vector database.
- The system does not quote price automatically.
- The system does not promise stock availability.
- The system does not promise lead time.
- The system does not send emails automatically.
- English reply drafts must be reviewed by a sales user.
- Login, CRM, ERP, live email integration, Qdrant, Redis, and quotation workflows are not connected yet.

## 14. Roadmap

Recommended next steps:

- Record a short 3-5 minute demo video using the captured screenshot flow.
- Add Alembic migrations for production database management.
- Replace lightweight keyword RAG with Qdrant.
- Add Redis for async jobs and workflow queues.
- Add authentication and role-based access control.
- Add CRM/ERP/email integrations.
- Add a quotation-preparation workflow with manual approval gates.
- Add production observability: logs, metrics, tracing, and audit events.

## 15. Resume Highlights

- Built a full-stack AI Agent application for B2B industrial automation export inquiry qualification.
- Designed a structured Agent workflow with fallback extraction, lightweight RAG, product matching, risk checking, and trace observability.
- Implemented FastAPI APIs, PostgreSQL persistence, Next.js frontend, and Docker Compose deployment.
- Applied human-in-the-loop design to avoid unsafe automation such as automatic quotation or delivery promises.

See [docs/resume_description.md](docs/resume_description.md) for bilingual resume-ready descriptions.
