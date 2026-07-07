# Manual Test Report

## 1. Test Environment

| Item | Value |
| --- | --- |
| Test date | 2026-07-07 |
| Startup mode | Docker Compose |
| Frontend | `http://127.0.0.1:3001` |
| Backend | `http://127.0.0.1:8000` |
| Swagger | `http://127.0.0.1:8000/docs` |
| Database | PostgreSQL in Docker Compose |
| Git branch | `master` |
| Validation baseline commit | `37acae631ef98c0f1b494b98475d091916c5f346` |
| Docker services | `industrial-agent-postgres`, `industrial-agent-backend`, `industrial-agent-frontend` |

Docker Compose status during validation:

| Service | Result | Notes |
| --- | --- | --- |
| `industrial-agent-postgres` | PASS | Container was running and healthy. |
| `industrial-agent-backend` | PASS | Container was running and healthy, mapped to `127.0.0.1:8000`. |
| `industrial-agent-frontend` | PASS | Container was running and healthy, mapped to `127.0.0.1:3001`. |

## 2. P0 Test Results

The following P0 items are recorded as PASS based on the user's completed end-to-end manual validation. They are not presented as newly re-clicked by Codex in this report round.

| Priority | Test Case | Result | Notes |
| --- | --- | --- | --- |
| P0 | Docker Compose three containers healthy | PASS | Confirmed by user's manual validation and current `docker-compose ps`. |
| P0 | Dashboard backend health normal | PASS | User manually confirmed dashboard health display. |
| P0 | `/analyze` can load sample inquiries and submit analysis | PASS | User manually confirmed. |
| P0 | AgentResult displays correctly | PASS | User manually confirmed. |
| P0 | Empty message blocks submission | PASS | User manually confirmed. |
| P0 | `/inquiries` shows newly created inquiries | PASS | User manually confirmed. |
| P0 | `/inquiries/{id}` shows inquiry detail | PASS | User manually confirmed. |
| P0 | Review can be submitted and appears in Review Logs | PASS | User manually confirmed. |
| P0 | Data remains after backend restart | PASS | User manually confirmed PostgreSQL persistence. |
| P0 | No automatic quotation, stock promise, lead-time promise, or email sending | PASS | User manually confirmed project boundary behavior. |

## 3. P1 Test Results

| Priority | Test Case | Result | Notes |
| --- | --- | --- | --- |
| P1 | PLC sample | PASS | API analysis succeeded. Returned `product_category=PLC`, 5 matched products, 2 missing fields, 4 retrieved knowledge chunks, 10 trace steps, reply draft present. |
| P1 | VFD sample | PASS | API analysis succeeded. Returned `product_category=VFD`, 5 matched products, 1 missing field, 4 retrieved knowledge chunks, 10 trace steps, reply draft present. |
| P1 | HMI sample | PASS | API analysis succeeded. Returned `product_category=HMI`, 5 matched products, 1 missing field, 4 retrieved knowledge chunks, 10 trace steps, reply draft present. |
| P1 | Industrial Switch sample | PASS | API analysis succeeded. Returned `product_category=Industrial Switch`, 5 matched products, 2 missing fields, 4 retrieved knowledge chunks, 10 trace steps, reply draft present. |
| P1 | Status/channel filtering | PASS | Browser validation on `/inquiries`: status filter reduced list from 10 to 3 rows, adding `website` channel reduced to 2 rows, clearing filters restored 10 rows, detail page opened successfully. |
| P1 | Swagger API visibility and basic API calls | PASS | OpenAPI contained required paths: `/api/health`, `/api/inquiries/analyze`, `/api/inquiries`, `/api/inquiries/{inquiry_id}`, `/api/inquiries/{inquiry_id}/review`, `/api/inquiries/samples`. `health`, `inquiries`, and `samples` requests succeeded. |
| P1 | Browser console | PASS | Browser console check found 0 frontend page errors on `/`, `/analyze`, `/inquiries`, and `/inquiries/10`. |
| P1 | Backend pytest | PASS | `python -m pytest` passed: 7 tests passed. Warnings were deprecation warnings, not blocking failures. |
| P1 | Frontend build | PASS | `npm run build` completed successfully. TypeScript/build checks passed with no blocking build errors. |

## 4. P2 Optional Test Items

The following items are optional / future validation:

| Priority | Test Case | Result | Notes |
| --- | --- | --- | --- |
| P2 | Frontend error prompt when backend is stopped | NOT EXECUTED | Future negative-path validation. |
| P2 | Direct PostgreSQL table query | NOT EXECUTED | Future database audit validation. |
| P2 | Long-text inquiry | NOT EXECUTED | Future robustness validation. |
| P2 | Irrelevant inquiry | NOT EXECUTED | Future intent/risk boundary validation. |
| P2 | Narrow-screen responsive display | NOT EXECUTED | Future UI responsive validation. |

## 5. Known Boundaries

- Current product data is high-fidelity simulated data.
- Current lightweight RAG is not a final production-grade vector database.
- The system does not quote price automatically.
- The system does not promise stock availability.
- The system does not promise lead time.
- The system does not send emails automatically.
- English reply drafts must be reviewed by a sales user before any external communication.
- Login, CRM, ERP, email system integration, Qdrant, and Redis are not connected yet.
- The current evaluation is for prototype validation and does not represent real production accuracy.

## 6. Final Conclusion

The project has passed P0 end-to-end manual validation and is suitable for GitHub portfolio display, resume presentation, interview walkthrough, and 3-5 minute demo recording.

This project has completed the stable demo loop for stages A1-A5.5. It can be treated as the current stable showcase version before entering A6.

## 7. Next Step: A6 Qdrant RAG Enhancement

Recommended next step:

```text
A6: Replace the current lightweight keyword-based RAG with Qdrant-based vector retrieval.
```

Suggested A6 scope:

1. Add Qdrant service to `docker-compose.yml`.
2. Add backend Qdrant configuration.
3. Split Markdown knowledge files into chunks and write them into Qdrant.
4. Add an embedding layer.
5. Make the Retriever support Qdrant search.
6. Keep keyword fallback.
7. Preserve the current `retrieved_knowledge` structure in `AgentResult`.
8. Keep the current frontend Retrieved Knowledge display working.
9. Add tests for Qdrant retrieval and fallback behavior.
10. Update README and docs.

A6 should not include:

- Knowledge base upload admin UI.
- Login or permission system.
- Redis.
- Email system integration.
- CRM/ERP integration.
- Quotation system.
