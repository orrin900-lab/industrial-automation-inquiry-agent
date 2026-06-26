# Industrial Inquiry Agent

A-stage engineering project for the Industrial Automation Inquiry Qualification Agent.

Current round: A4 Docker Compose one-command startup for PostgreSQL, FastAPI backend, and Next.js frontend.

The C+ Streamlit prototype remains in:

```text
../industrial-inquiry-agent-cplus
```

## Services

- `postgres`: PostgreSQL database for persisted inquiries, AgentResult, AgentRun, AgentStep, and review logs.
- `backend`: FastAPI wrapper around the Agent Core.
- `frontend`: Next.js customer service and export sales console.

## Docker Compose

From this project root:

```bash
docker compose up --build
```

If your Docker CLI does not expose the `docker compose` subcommand, use the installed standalone Compose command:

```bash
docker-compose up --build
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
docker compose down
```

Standalone Compose equivalent:

```bash
docker-compose down
```

Stop services and clear the PostgreSQL volume:

```bash
docker compose down -v
```

Standalone Compose equivalent:

```bash
docker-compose down -v
```

Docker Compose uses PostgreSQL by default:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/industrial_agent
```

## Manual Backend

Manual startup is still available and keeps the SQLite fallback unless `DATABASE_URL` is set:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

## Manual Frontend

```bash
cd frontend
npm install
npm run dev -- -H 127.0.0.1 -p 3001
```

Frontend URL:

```text
http://127.0.0.1:3001
```

Backend API base URL:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

## Validation

```bash
cd backend
pytest
```

```bash
cd frontend
npm run build
```

After Docker Compose starts, verify:

- `GET http://127.0.0.1:8000/api/health`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:3001`
- Analyze inquiry flow
- Inquiry list and detail pages
- Review submission

## Business Boundaries

The system does not quote price, promise stock, promise lead time, or send emails automatically. It generates structured analysis and an English reply draft for manual review only.
