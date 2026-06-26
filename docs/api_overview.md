# API Overview

Base URL:

```text
http://127.0.0.1:8000
```

## GET /api/health

Purpose: Check backend availability.

Request:

```bash
curl http://127.0.0.1:8000/api/health
```

Response:

```json
{
  "status": "ok",
  "service": "industrial-inquiry-agent-backend"
}
```

Database write: No.

Triggers Agent: No.

Requires human review: No.

## POST /api/inquiries/analyze

Purpose: Save an inquiry, run the Agent workflow, save the AgentResult and trace, and return structured analysis.

Request:

```json
{
  "channel": "website",
  "customer_name": "John Smith",
  "customer_email": "john@example.com",
  "company": "ABC Automation",
  "country": "Vietnam",
  "subject": "PLC inquiry",
  "message": "We need a Siemens compatible PLC with 16DI and 8DO, 24V DC, RS485 communication.",
  "attachments": []
}
```

Response:

```json
{
  "status": "success",
  "inquiry_id": 1,
  "agent_result_id": 1,
  "agent_result": {
    "inquiry_type": "website",
    "customer_intent": "product_selection",
    "product_category": "PLC",
    "extracted_requirements": {
      "product_category": "PLC",
      "brand": "Siemens",
      "technical_specs": {
        "digital_inputs": "16DI",
        "digital_outputs": "8DO",
        "power_supply": "24V DC",
        "communication": "RS485"
      }
    },
    "missing_information": ["output_type"],
    "matched_products": [],
    "clarification_questions": [],
    "english_reply_draft": "Thank you for your inquiry...",
    "risk_flags": [],
    "sales_follow_up_suggestion": "Confirm missing parameters before quotation.",
    "confidence_score": 0.82,
    "agent_trace": [],
    "retrieved_knowledge": []
  }
}
```

Database write: Yes. Writes inquiry, AgentResult, AgentRun, and AgentStep records.

Triggers Agent: Yes.

Requires human review: Yes, before any customer-facing reply.

## GET /api/inquiries

Purpose: Return persisted inquiry list.

Query parameters:

- `status`
- `channel`
- `product_category`
- `limit`
- `offset`

Request:

```bash
curl "http://127.0.0.1:8000/api/inquiries?limit=10"
```

Response:

```json
{
  "status": "success",
  "items": [
    {
      "id": 1,
      "channel": "website",
      "customer_name": "John Smith",
      "company": "ABC Automation",
      "country": "Vietnam",
      "subject": "PLC inquiry",
      "status": "pending_review",
      "product_category": "PLC",
      "confidence_score": 0.82,
      "created_at": "2026-06-26T10:00:00",
      "updated_at": "2026-06-26T10:00:00"
    }
  ],
  "limit": 10,
  "offset": 0
}
```

Database write: No.

Triggers Agent: No.

Requires human review: No, but returned records may be pending review.

## GET /api/inquiries/{id}

Purpose: Return inquiry detail, latest AgentResult, and review logs.

Request:

```bash
curl http://127.0.0.1:8000/api/inquiries/1
```

Response:

```json
{
  "inquiry": {
    "id": 1,
    "channel": "website",
    "customer_name": "John Smith",
    "customer_email": "john@example.com",
    "company": "ABC Automation",
    "country": "Vietnam",
    "subject": "PLC inquiry",
    "message": "We need a Siemens compatible PLC...",
    "status": "pending_review"
  },
  "agent_result": {
    "product_category": "PLC",
    "matched_products": [],
    "agent_trace": [],
    "retrieved_knowledge": []
  },
  "review_logs": []
}
```

Database write: No.

Triggers Agent: No.

Requires human review: The detail page is designed for human review.

## POST /api/inquiries/{id}/review

Purpose: Save a human review decision and edited reply draft.

Request:

```json
{
  "reviewer_name": "Sales User",
  "review_status": "need_clarification",
  "edited_reply": "Thank you for your inquiry...",
  "reviewer_note": "Need to confirm output type."
}
```

Response:

```json
{
  "status": "success",
  "inquiry_id": 1,
  "review_status": "need_clarification"
}
```

Database write: Yes. Writes review log and updates inquiry status.

Triggers Agent: No.

Requires human review: This endpoint records the review.

## GET /api/inquiries/samples

Purpose: Return synthetic demo inquiries for frontend loading.

Request:

```bash
curl http://127.0.0.1:8000/api/inquiries/samples
```

Response:

```json
{
  "status": "success",
  "samples": [
    {
      "id": "inq_plc_001",
      "channel": "website",
      "subject": "PLC module inquiry",
      "message": "We need a Siemens compatible PLC...",
      "expected_category": "PLC"
    }
  ]
}
```

Database write: No.

Triggers Agent: No.

Requires human review: No.

## Boundary

APIs do not quote price, promise stock, promise lead time, or send emails automatically. Reply drafts are internal and must be reviewed by a sales user.
