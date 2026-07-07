# 演示脚本 Demo Script

推荐录屏时长：3-5 分钟。

推荐样例：PLC sample 或 VFD sample。PLC 样例适合展示缺失 output_type、候选产品、RAG 来源和 fallback trace。

## 1. 启动项目

```bash
cd industrial-inquiry-agent
docker-compose up --build
```

打开：

```text
Frontend: http://127.0.0.1:3001
Backend API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs
```

讲解：

> 这是一个面向工业自动化外贸询盘的 full-stack AI Agent 项目。Docker Compose 会启动 PostgreSQL、FastAPI backend 和 Next.js 前端后台。

## 2. Dashboard 首页

展示：

- Backend health。
- 总询盘数。
- 待审核数量。
- 最近询盘。
- 中英文语言切换。

截图：`docs/screenshots/01_dashboard.png`

## 3. Analyze Inquiry 询盘分析

步骤：

1. 打开 Analyze 页面。
2. 加载 PLC 或 VFD sample。
3. 提交分析。

截图：`docs/screenshots/02_analyze_form.png`

讲解：

> 系统会保存原始询盘，运行 Agent workflow，并返回结构化 AgentResult。

## 4. AgentResult 结构化结果

展示：

- Inquiry Type。
- Customer Intent。
- Product Category。
- Confidence Score。
- Extracted Requirements。
- Clarification Questions。

截图：`docs/screenshots/03_agent_result.png`

## 5. Candidate Products 候选产品

展示：

- product_id。
- product_name。
- match_score。
- match_reason。
- missing_confirmations。

截图：`docs/screenshots/06_candidate_products.png`

## 6. Retrieved Knowledge 检索来源

展示：

- source_file。
- section_title。
- score。
- content preview。

截图：`docs/screenshots/07_retrieved_knowledge.png`

讲解：

> 当前使用 lightweight Markdown RAG，下一轮 A6 可以替换为 Qdrant。

## 7. Agent Trace 执行轨迹

展示：

- step_name。
- mode: rule / fallback / retrieval。
- success。
- latency_ms。
- output_summary。

截图：`docs/screenshots/08_agent_trace.png`

## 8. Inquiry Detail 详情页

展示：

- Original Inquiry。
- AgentResult。
- Risk Flags。
- English Reply Draft。

截图：`docs/screenshots/05_inquiry_detail.png`

## 9. Human Review 人工审核

步骤：

1. 检查 English Reply Draft。
2. 填写 reviewer_note。
3. 提交 review_status。
4. 查看 Review Logs。

截图：`docs/screenshots/09_review_form.png`

讲解：

> Review 只记录人工审核状态和草稿，不会自动发送邮件。

## 10. Swagger API

打开 `http://127.0.0.1:8000/docs`。

展示：

- `GET /api/health`
- `POST /api/inquiries/analyze`
- `GET /api/inquiries`
- `GET /api/inquiries/{id}`
- `POST /api/inquiries/{id}/review`
- `GET /api/inquiries/samples`

截图：`docs/screenshots/10_swagger_api.png`

## 11. 结尾边界说明

结尾必须说明：

- 当前使用高仿真模拟数据。
- 不自动报价。
- 不承诺库存。
- 不承诺交期。
- 不自动发送邮件。
- 英文回复草稿必须人工审核。
- 当前轻量 RAG 不是最终生产级向量数据库。
