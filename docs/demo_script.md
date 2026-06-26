# Demo Script

This script is intended for a short recording, GitHub demo, or interview walkthrough.

## 1. Start The Project

```bash
cd D:\Codex项目文件夹\外贸客服Agent\industrial-inquiry-agent
docker-compose up --build
```

Open:

```text
Frontend: http://127.0.0.1:3001
Backend API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs
```

Narration:

"This project is a full-stack AI Agent application for industrial automation export inquiry qualification. Docker Compose starts PostgreSQL, FastAPI, and the Next.js sales console."

## 2. Dashboard

Open `http://127.0.0.1:3001`.

Show:

- Backend health.
- Total inquiries.
- Pending review count.
- Analyzed count.
- Recent inquiries.

Narration:

"The dashboard confirms that the frontend can reach the FastAPI backend and shows persisted inquiry records from PostgreSQL."

## 3. Analyze Inquiry

Go to `Analyze Inquiry`.

Steps:

1. Load a sample inquiry.
2. Choose Website Inquiry or Email Inquiry.
3. Submit analysis.

Narration:

"The user can paste a raw customer inquiry or load a demo sample. The backend persists the inquiry, runs the Agent workflow, stores the result and trace, then returns a structured AgentResult."

## 4. AgentResult

Show:

- Inquiry type.
- Customer intent.
- Product category.
- Confidence score.
- Extracted requirements.
- Clarification questions.
- Sales follow-up suggestion.

Narration:

"The AgentResult is structured JSON under the hood, not just a free-form LLM answer. This makes it easier to persist, audit, and display."

## 5. Candidate Products

Show candidate products.

Narration:

"Candidate products come from the product repository, not from hallucinated LLM output. Each candidate has a match score, match reason, and missing confirmations."

## 6. Missing Information

Show missing information and clarification questions.

Narration:

"The system is not trying to close the deal automatically. It identifies what still needs to be confirmed, such as output type, communication protocol, voltage, or quantity."

## 7. Retrieved Knowledge

Show Retrieved Knowledge Sources.

Narration:

"The current prototype uses a lightweight Markdown RAG pipeline. Each retrieved source includes metadata, score, and content preview. Later this retriever can be replaced by Qdrant."

## 8. Agent Trace

Show Agent Execution Trace.

Narration:

"The trace records which steps ran, whether they used rule, fallback, retrieval, or hybrid mode, and how long each step took. This is useful for debugging and trust."

## 9. Inquiry Detail

Click View Detail.

Show:

- Original inquiry.
- AgentResult sections.
- English reply draft.
- Risk flags.
- Review form.

Narration:

"The detail page is designed for the sales user to review the AI output before taking action."

## 10. Edit Reply Draft And Submit Review

Steps:

1. Edit the English Reply Draft.
2. Fill reviewer note.
3. Submit review as `need_clarification`, `ready_for_quotation`, or another status.
4. Show Review Logs.

Narration:

"The review action only records a human decision. It does not send email and does not quote price."

## 11. Inquiry List

Open Inquiry List.

Show:

- Persisted inquiry rows.
- Status filter.
- Channel filter.
- Detail links.

Narration:

"The inquiry list is backed by PostgreSQL. Docker Compose uses a named volume so data remains after restarting containers."

## 12. Boundary Statement

End the demo with:

"This prototype uses high-fidelity simulated data. It does not quote price, promise stock, promise lead time, or send emails automatically. It is an AI-assisted workflow with human review, not an autonomous sales closer."
