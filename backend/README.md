# Industrial Inquiry Agent Backend

FastAPI backend for the A-stage industrial inquiry agent. A1 wrapped the C+ Agent Core. A2 adds database persistence for inquiries, AgentResult, AgentRun, AgentStep, and human review logs.

The backend still does not quote price, promise stock, promise lead time, or send emails automatically.

## Docker

The backend is included in the root Docker Compose stack:

```bash
cd ..
docker compose up --build
```

If `docker compose` is unavailable locally:

```bash
cd ..
docker-compose up --build
```

Docker Compose uses PostgreSQL by default:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/industrial_agent
ENABLE_LLM_EXTRACTION=false
```

The backend container exposes:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
```

Tables are created automatically at startup. The startup code retries database initialization so the backend can wait for PostgreSQL readiness.

## Database

Default local database:

```env
DATABASE_URL=sqlite:///./storage/dev.db
```

PostgreSQL example:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/industrial_agent
```

Tables are created automatically on local startup. Alembic migrations can be added in a later engineering round.

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

Swagger:

```text
http://localhost:8000/docs
```

Health:

```text
http://localhost:8000/api/health
```

## Test

```bash
pytest
```

If the local shell cannot import `app`, run:

```bash
PYTHONPATH=. pytest
```

## APIs

- `GET /api/health`
- `POST /api/inquiries/analyze`
- `GET /api/inquiries/samples`
- `GET /api/inquiries`
- `GET /api/inquiries/{inquiry_id}`
- `POST /api/inquiries/{inquiry_id}/review`

`POST /api/inquiries/analyze` persists the inquiry, AgentResult, AgentRun, and AgentStep trace records, then returns `inquiry_id`, `agent_result_id`, and `agent_result`.
