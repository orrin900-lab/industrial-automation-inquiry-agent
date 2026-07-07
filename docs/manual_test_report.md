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
| Git branch | `master` |
| Baseline commit | `37acae631ef98c0f1b494b98475d091916c5f346` |

## 2. P0 测试结果

以下 P0 项由用户完成端到端人工复测，本报告按用户复测结论记录为 PASS。

| Priority | Test Case | Result | Notes |
| --- | --- | --- | --- |
| P0 | Docker Compose 三容器 healthy | PASS | 用户已人工确认。 |
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
| P1 | VFD sample | PASS | 返回 `product_category=VFD`，候选产品、RAG、Trace、reply draft 均存在。 |
| P1 | HMI sample | PASS | 返回 `product_category=HMI`，候选产品、RAG、Trace、reply draft 均存在。 |
| P1 | Industrial Switch sample | PASS | 返回 `product_category=Industrial Switch`，候选产品、RAG、Trace、reply draft 均存在。 |
| P1 | status/channel 筛选 | PASS | 浏览器验证筛选可切换、可清除，并可进入详情页。 |
| P1 | Swagger API | PASS | 关键 API path 可见，`health`、`inquiries`、`samples` 请求成功。 |
| P1 | Browser console | PASS | `/`、`/analyze`、`/inquiries`、`/inquiries/10` 无明显 console error。 |
| P1 | backend pytest | PASS | `7 passed`。 |
| P1 | frontend build | PASS | `npm run build` 成功。 |

## 4. P2 可选测试项

| Priority | Test Case | Result | Notes |
| --- | --- | --- | --- |
| P2 | 后端关闭时前端错误提示 | NOT EXECUTED | 后续负向测试。 |
| P2 | PostgreSQL 表数据直接查询 | NOT EXECUTED | 后续数据库审计测试。 |
| P2 | 长文本询盘 | NOT EXECUTED | 后续鲁棒性测试。 |
| P2 | 无关询盘 | NOT EXECUTED | 后续边界测试。 |
| P2 | 窄屏页面显示 | NOT EXECUTED | 后续响应式测试。 |

## 5. 已知边界 Known Boundaries

- 当前产品数据为高仿真模拟数据。
- 当前轻量 RAG 不是最终生产级向量数据库。
- 当前不自动报价。
- 当前不承诺库存。
- 当前不承诺交期。
- 当前不自动发送邮件。
- English Reply Draft 必须由业务员人工审核。
- 登录权限、CRM、ERP、邮件系统、Qdrant、Redis 尚未接入。
- 当前评估不代表真实生产准确率。

## 6. 最终结论 Final Conclusion

The project has passed P0 end-to-end manual validation and is suitable for GitHub portfolio display, resume presentation, interview walkthrough, and 3-5 minute demo recording.

中文结论：当前项目已通过 P0/P1 阶段复测，可以作为稳定展示版本。

## 7. 下一步 A6：Qdrant RAG Enhancement

建议下一轮：

```text
A6: Replace the current lightweight keyword-based RAG with Qdrant-based vector retrieval.
```

A6 暂不做：

- 知识库上传后台。
- 登录权限。
- Redis。
- 邮件系统。
- CRM/ERP。
- 报价系统。
