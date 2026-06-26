# Screenshots

This directory contains real screenshots captured from the running Docker Compose stack. Do not add fake screenshots.

| File | Status | What It Shows |
| --- | --- | --- |
| `01_dashboard.png` | captured | Dashboard with backend health, statistics, recent inquiries, and navigation entry points. |
| `02_analyze_form.png` | captured | Analyze Inquiry form with sample inquiry loading, channel selector, message box, and analyze button. |
| `03_agent_result.png` | captured | Structured AgentResult summary, extracted requirements, clarification questions, and follow-up suggestion. |
| `04_inquiry_list.png` | captured | Inquiry list table with persisted records, status/category/confidence fields, and filters. |
| `05_inquiry_detail.png` | captured | Inquiry detail top section with original inquiry and AgentResult summary area. |
| `06_candidate_products.png` | captured | Candidate product recommendations with product IDs, match scores, match reasons, and missing confirmations. |
| `07_retrieved_knowledge.png` | captured | Retrieved Knowledge Sources from the lightweight Markdown RAG retriever. |
| `08_agent_trace.png` | captured | Agent Execution Trace with node mode, success status, latency, and output summary. |
| `09_review_form.png` | captured | English reply draft, human review form, review status, reviewer note, and Review Logs area. |
| `10_swagger_api.png` | captured | FastAPI Swagger documentation with the main inquiry APIs. |
| `11_docker_compose_running.png` | pending | Docker Desktop or terminal output showing postgres, backend, and frontend containers as healthy. |

The Docker status screenshot is still pending because the automated browser tool could not capture a terminal/data-rendered page under its security policy. The underlying `docker-compose ps` verification was performed against the real running stack.

## Suggested Capture Flow

1. Start the stack with `docker-compose up --build` or `docker-compose up -d`.
2. Open `http://127.0.0.1:3001`.
3. Capture the dashboard.
4. Open Analyze Inquiry and load a PLC or VFD sample.
5. Submit the inquiry and capture AgentResult sections.
6. Open the detail page and capture candidate products, RAG sources, Agent Trace, and Review Form.
7. Open `http://127.0.0.1:8000/docs` for Swagger.
8. Capture Docker Desktop or terminal showing the three healthy containers.
