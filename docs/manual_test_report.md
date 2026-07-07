# 人工复测报告 Manual Test Report

## 1. 测试环境 Test Environment

| Item | Value |
| --- | --- |
| Test date | 2026-07-07 |
| Startup mode | Docker Compose |
| Frontend | `http://127.0.0.1:3001` |
| Backend | `http://127.0.0.1:8000` |
| Swagger | `http://127.0.0.1:8000/docs` |
| Database | PostgreSQL in Docker Compose |
| Vector DB | Qdrant in Docker Compose |
| Git branch | `feature/qdrant-rag` |

## 2. P0 测试结果

以下 P0 项由用户在 A5 阶段完成端到端人工复测，本报告按用户复测结论记录为 PASS。

| Priority | Test Case | Result | Notes |
| --- | --- | --- | --- |
| P0 | Docker Compose 三容器 healthy | PASS | 用户已人工确认。A6 后扩展为四服务。 |
| P0 | Dashboard backend health 正常 | PASS | 用户已人工确认。 |
| P0 | `/analyze` 可加载样例并提交询盘 | PASS | 用户已人工确认。 |
| P0 | AgentResult 正常展示 | PASS | 用户已人工确认。 |
| P0 | 空 message 会阻止提交 | PASS | 用户已人工确认。 |
| P0 | `/inquiries` 能看到新增询盘 | PASS | 用户已人工确认。 |
| P0 | `/inquiries/{id}` 能看到详情 | PASS | 用户已人工确认。 |
| P0 | review 可以提交并显示在 Review Logs | PASS | 用户已人工确认。 |
| P0 | 重启 backend 后数据仍存在 | PASS | 用户已人工确认。 |
| P0 | 不自动报价、不承诺库存、不承诺交期、不自动发送邮件 | PASS | 用户已人工确认。 |

## 3. P1 测试结果

| Priority | Test Case | Result | Notes |
| --- | --- | --- | --- |
| P1 | PLC sample | PASS | 返回 `product_category=PLC`，候选产品、RAG、Trace、reply draft 均存在。 |
| P1 | VFD sample | PASS | A5 阶段已通过。 |
| P1 | HMI sample | PASS | A5 阶段已通过。 |
| P1 | Industrial Switch sample | PASS | A5 阶段已通过。 |
| P1 | status/channel 筛选 | PASS | A5 阶段已通过。 |
| P1 | Swagger API | PASS | `http://127.0.0.1:8000/docs` 返回 200。 |
| P1 | Browser console | PASS | A6 验证核心页面 console error count = 0。 |
| P1 | backend pytest | PASS | A6 后 `14 passed`。 |
| P1 | frontend build | PASS | `npm run build` 成功。 |

## 4. A6 Qdrant RAG 验证结果

| Test Case | Result | Notes |
| --- | --- | --- |
| Docker Compose config | PASS | `docker-compose config --quiet` 通过。 |
| Docker Compose startup | PASS | postgres、backend、frontend healthy，qdrant running。 |
| Qdrant API | PASS | `http://127.0.0.1:6333` 返回 200。 |
| Qdrant collection | PASS | `industrial_agent_knowledge` 创建成功。 |
| Qdrant chunks | PASS | `chunks_loaded=21`，`chunks_upserted=21`，`points_count=21`。 |
| Analyze API | PASS | PLC sample 返回 `product_category=PLC`。 |
| Retrieval mode | PASS | Agent Trace 中 `Knowledge Retriever=qdrant`。 |
| Retrieved Knowledge | PASS | 返回 4 条知识来源，结构保持 `content/score/metadata`。 |
| Inquiry list/detail | PASS | `/api/inquiries` 和 `/api/inquiries/12` 正常。 |
| Review API | PASS | `/api/inquiries/12/review` 返回 success。 |
| Qdrant fallback unit test | PASS | Qdrant 不可用时 fallback 到 keyword retriever。 |

## 5. P2 可选测试项

| Priority | Test Case | Result | Notes |
| --- | --- | --- | --- |
| P2 | 后端关闭时前端错误提示 | NOT EXECUTED | 后续负向测试。 |
| P2 | PostgreSQL 表数据直接查询 | NOT EXECUTED | 后续数据库审计测试。 |
| P2 | 长文本询盘 | NOT EXECUTED | 后续鲁棒性测试。 |
| P2 | 无关询盘 | NOT EXECUTED | 后续边界测试。 |
| P2 | 窄屏页面显示 | NOT EXECUTED | 后续响应式测试。 |

## 6. 已知边界 Known Boundaries

- 当前产品数据为高仿真模拟数据。
- 当前 hashing embedding 是 prototype lightweight embedding，不代表最终生产语义 embedding。
- 当前 Qdrant RAG 已具备工程接口，但后续仍可升级为 OpenAI embeddings 或 sentence-transformers。
- 当前不自动报价。
- 当前不承诺库存。
- 当前不承诺交期。
- 当前不自动发送邮件。
- English Reply Draft 必须由业务员人工审核。
- 登录权限、CRM、ERP、邮件系统、Redis、报价系统尚未接入。
- 当前评估不代表真实生产准确率。

## 7. 最终结论 Final Conclusion

The project has passed P0 end-to-end manual validation and A6 Qdrant RAG engineering validation. It is suitable for GitHub portfolio display, resume presentation, interview walkthrough, and 3-5 minute demo recording.

中文结论：当前项目已经具备 FastAPI、Next.js、PostgreSQL、Qdrant、Docker Compose、Agent Trace、Retrieved Knowledge 和 Human Review 的完整展示闭环，可以作为稳定作品集项目继续迭代。

## 8. 下一步建议

建议下一轮优先选择：

```text
Knowledge Base Admin: add a lightweight backend/frontend flow for viewing knowledge chunks and rebuilding Qdrant index.
```

也可以先做最终简历 / 面试材料整理，将 A6 Qdrant 能力纳入 resume bullets 和 demo script。
