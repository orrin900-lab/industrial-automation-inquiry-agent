# API 概览 API Overview

Backend base URL:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## 1. GET /api/health

功能：健康检查。

- 是否写数据库：否。
- 是否触发 Agent：否。
- 是否需要人工审核：否。

响应示例：

```json
{
  "status": "ok",
  "service": "industrial-inquiry-agent-backend"
}
```

## 2. POST /api/inquiries/analyze

功能：提交询盘并运行 Agent 分析。

- 是否写数据库：是，保存 inquiry、agent_result、agent_run、agent_steps。
- 是否触发 Agent：是。
- 是否触发 RAG：是，优先 Qdrant，失败时 keyword fallback。
- 是否需要人工审核：是，返回的英文回复草稿必须人工审核。

请求示例：

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

响应示例：

```json
{
  "status": "success",
  "inquiry_id": 1,
  "agent_result_id": 1,
  "agent_result": {
    "inquiry_type": "replacement_request",
    "customer_intent": "...",
    "product_category": "PLC",
    "extracted_requirements": {},
    "missing_information": [],
    "matched_products": [],
    "clarification_questions": [],
    "english_reply_draft": "...",
    "risk_flags": [],
    "sales_follow_up_suggestion": "...",
    "confidence_score": 0.61,
    "agent_trace": [],
    "retrieved_knowledge": []
  }
}
```

`retrieved_knowledge` 结构：

```json
{
  "content": "...",
  "score": 0.91,
  "metadata": {
    "source_file": "selection_rules.md",
    "section_title": "PLC Selection",
    "document_type": "selection_rules",
    "chunk_id": "selection_rules.md:1:1"
  }
}
```

## 3. GET /api/inquiries

功能：查询询盘列表。

- 是否写数据库：否。
- 是否触发 Agent：否。
- 是否需要人工审核：列表用于进入人工审核工作流。

可选参数：

```text
status
channel
product_category
limit
offset
```

响应字段包括：

```text
id
channel
customer_name
company
country
subject
status
product_category
confidence_score
created_at
updated_at
```

## 4. GET /api/inquiries/{id}

功能：查询询盘详情。

- 是否写数据库：否。
- 是否触发 Agent：否。
- 是否需要人工审核：用于人工查看 AgentResult 并提交 Review。

响应结构：

```json
{
  "inquiry": {},
  "agent_result": {},
  "review_logs": []
}
```

## 5. POST /api/inquiries/{id}/review

功能：提交人工审核结果。

- 是否写数据库：是，保存 review_log 并更新 inquiry status。
- 是否触发 Agent：否。
- 是否需要人工审核：这就是人工审核动作。

请求示例：

```json
{
  "reviewer_name": "Sales User",
  "review_status": "need_clarification",
  "edited_reply": "Thank you for your inquiry...",
  "reviewer_note": "Need to confirm output type."
}
```

响应示例：

```json
{
  "status": "success",
  "inquiry_id": 1,
  "review_status": "need_clarification"
}
```

注意：该 API 不发送邮件，只记录人工审核状态和编辑草稿。

## 6. GET /api/inquiries/samples

功能：读取样例询盘。

- 是否写数据库：否。
- 是否触发 Agent：否。
- 是否需要人工审核：否。

用途：前端 Analyze 页面加载 PLC / VFD / HMI / Industrial Switch 样例。

## 7. Qdrant Index Build

Qdrant 索引构建不是 HTTP API，而是后端脚本：

```bash
docker-compose exec backend python scripts/build_qdrant_index.py
```

或本地运行：

```bash
cd backend
python scripts/build_qdrant_index.py
```

该脚本会读取 Markdown 知识库，切分 chunks，使用 hashing embedding 生成向量，并 upsert 到 Qdrant collection。

## 8. 边界说明

API 不提供：

- 自动报价。
- 库存承诺。
- 交期承诺。
- 自动邮件发送。
- 登录权限。
- CRM / ERP 集成。
