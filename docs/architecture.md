# Architecture

## Current System Architecture

```mermaid
flowchart TD
    U[Sales User / Operator] --> F[Next.js Frontend]
    F --> B[FastAPI Backend]
    B --> S[Agent Service]
    S --> A[Agent Core]
    A --> R[Lightweight RAG]
    A --> P[Product Repository]
    S --> DB[(PostgreSQL)]
    DB --> S
```

The system is an internal sales-assistance platform. Users submit customer inquiries through the Next.js frontend. FastAPI receives the request, persists the inquiry, invokes the Agent Core, stores the structured result and trace, and returns the analysis to the frontend.

## From C+ Prototype To A-Stage Engineering

The project evolved in two layers:

- C+ prototype: Streamlit demo, mock/fallback logic, Pydantic schemas, product CSV repository, lightweight RAG, AgentResult export, and batch demo evaluation.
- A-stage engineering: FastAPI wrapper, PostgreSQL persistence, Next.js sales console, review workflow, Docker Compose startup chain.

This staged approach made the agent workflow testable before adding enterprise-style infrastructure.

## Frontend, Backend, Database, And Agent Core

- Frontend: Next.js App Router console for dashboard, inquiry analysis, inquiry list, detail view, reply draft editing, and review submission.
- Backend: FastAPI service exposing REST endpoints under `/api`.
- Agent Core: classification, extraction, missing information check, retrieval, product matching, reply drafting, risk checking, and trace recording.
- Database: PostgreSQL stores inquiries, AgentResult records, AgentRun records, AgentStep trace records, and ReviewLog records.
- Repository layer: isolates product data and persistence from agent nodes.

## Docker Compose Services

```mermaid
flowchart LR
    Browser[Browser] --> FE[frontend container<br/>Next.js :3000]
    Browser --> BE[backend container<br/>FastAPI :8000]
    BE --> PG[postgres container<br/>PostgreSQL :5432]
```

Docker Compose services:

- `postgres`: stores persistent data in the `postgres_data` named volume.
- `backend`: connects to Postgres through `DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/industrial_agent`.
- `frontend`: serves the Next.js app on container port `3000`, mapped to host `127.0.0.1:3001`.

## Lightweight RAG And Future Qdrant Replacement

Current RAG is intentionally lightweight:

- Loads Markdown files from `backend/data/`.
- Splits documents into chunks by heading.
- Keeps metadata such as source file, section title, document type, and chunk id.
- Uses keyword scoring for retrieval.

Future Qdrant integration point:

```mermaid
flowchart TD
    A[Agent Core] --> RI[Retriever Interface]
    RI --> LR[Current Lightweight Retriever]
    RI --> QR[Future Qdrant Retriever]
```

The retriever interface keeps the Agent Core independent from the storage engine, making Qdrant a replaceable implementation rather than a workflow rewrite.

## Human-In-The-Loop Design

The system generates an English reply draft but does not send it. The sales user edits and reviews the draft, then submits a review status. This is important because industrial automation inquiries often involve:

- Price sensitivity.
- Stock uncertainty.
- Lead time uncertainty.
- Technical compatibility risk.
- Brand authorization and certification claims.

## Risk Control Boundary

The system explicitly avoids unsafe automation:

- No automatic price quotation.
- No stock availability promise.
- No lead time promise.
- No automatic email sending.
- No official brand compatibility claim without verification.
- No production CRM, ERP, email, Redis, Qdrant, or authentication integration yet.

Current product and inquiry data are high-fidelity simulated demo data.
