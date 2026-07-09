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
| Git branch | A6 validation on `feature/qdrant-rag`; stable merge target `master` |

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

| Priority | Test Case | Result | Notes |
| --- | --- | --- | --- |
| A6 | Docker Compose includes Qdrant | PASS | `docker-compose config` 显示 `qdrant` 服务和 `qdrant_data` volume。 |
| A6 | Qdrant endpoint reachable | PASS | `http://127.0.0.1:6333` 返回 200。 |
| A6 | Qdrant collection created | PASS | collection 为 `industrial_agent_knowledge`，状态 `green`。 |
| A6 | Knowledge chunks indexed | PASS | `chunks_loaded=21`，`chunks_upserted=21`，`points_count=21`。 |
| A6 | Stable upsert | PASS | 重复执行 index build 后 `points_count` 仍为 `21`，没有重复堆叠。 |
| A6 | Qdrant retrieval works | PASS | PLC sample 分析成功，Retrieved Knowledge 返回 4 条。 |
| A6 | Agent Trace shows qdrant mode | PASS | Knowledge Retriever 节点显示 `mode=qdrant`。 |
| A6 | Retrieved Knowledge compatible structure | PASS | 保持 `content`、`score`、`metadata.source_file/section_title/document_type/chunk_id`。 |
| A6 | Keyword fallback works | PASS | `test_qdrant_fallback.py` 覆盖 Qdrant 不可用时 fallback。 |
| A6 | Backend pytest | PASS | A6.5 回归结果：`14 passed`。 |
| A6 | Frontend build | PASS | `npm run build` 成功。 |
| A6 | Analyze workflow | PASS | `/api/inquiries/analyze` 返回 `product_category=PLC`，`retriever_mode=qdrant`。 |
| A6 | Review workflow | PASS | `/api/inquiries/{id}/review` 返回 success。 |

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

## 9. A7 Knowledge Base Admin 验证结果

| Priority | Test Case | Result | Notes |
| --- | --- | --- | --- |
| A7 | Branch created | PASS | 当前开发分支为 `feature/knowledge-base-admin`。 |
| A7 | Backend Knowledge API registered | PASS | 新增 `/api/knowledge/status`、`/api/knowledge/chunks`、`/api/knowledge/reindex`。 |
| A7 | Qdrant status API | PASS | `rag_mode=qdrant`，`qdrant_available=true`，`points_count=21`。 |
| A7 | Chunks API | PASS | `GET /api/knowledge/chunks?limit=3&offset=0` 返回 `total=21` 和 Qdrant payload items。 |
| A7 | Reindex API | PASS | `POST /api/knowledge/reindex` 返回 `success=true`，`indexed_chunks=21`，`points_count=21`。 |
| A7 | `/knowledge` frontend page | PASS | `http://127.0.0.1:3001/knowledge` 返回 200。 |
| A7 | Chinese / English i18n | PASS | `/knowledge` 已接入现有轻量 i18n 字典和 AppShell 导航。 |
| A7 | Backend pytest | PASS | A7 后 `18 passed`。 |
| A7 | Frontend build | PASS | `npm run build` 成功，包含 `/knowledge` route。 |
| A7 | Docker Compose | PASS | postgres/backend/frontend healthy，qdrant running。 |
| A7 | Analyze workflow | PASS | PLC sample API 分析成功，`product_category=PLC`，Retrieved Knowledge 返回 4 条，Agent Trace 包含 `qdrant`。 |
| A7 | Review workflow | PASS | Review API 返回 `success`，状态为 `need_clarification`。 |

A7 当前只做轻量知识库运维：查看状态、查看 chunks、手动 rebuild index。未做上传、编辑、删除、登录权限、Redis、邮件系统、CRM/ERP 或报价系统。

## 10. A7.5 Knowledge Base Admin Browser Retest

| Priority | Test Case | Result | Notes |
| --- | --- | --- | --- |
| A7.5 | `/knowledge` 页面 | PASS | 浏览器访问 `http://127.0.0.1:3001/knowledge` 成功。 |
| A7.5 | Knowledge Status | PASS | 显示 `RAG Mode=qdrant`、`Collection=industrial_agent_knowledge`、`Vector Size=384`。 |
| A7.5 | Qdrant Available | PASS | 页面和 API 均显示 Qdrant available。 |
| A7.5 | points_count | PASS | `points_count=21`，重建后仍为 21。 |
| A7.5 | chunks list | PASS | chunks total 为 21，列表可展示 chunk_id、source_file、section_title、document_type、content_preview。 |
| A7.5 | source_file filter | PASS | 浏览器中按 `faq.md` 筛选成功。 |
| A7.5 | pagination / limit-offset | PASS | 全部来源下 Next 按钮可点击，页面内容变化；API 支持 `limit` / `offset`。 |
| A7.5 | Rebuild Index | PASS | 浏览器点击 `Rebuild Qdrant Index` 后显示 `Qdrant index rebuilt successfully.` |
| A7.5 | i18n | PASS | 中文默认展示正常，可切换到 English。 |
| A7.5 | Screenshots | PASS | 新增 `12_knowledge_base_admin.png` 和 `13_knowledge_reindex_success.png`。 |
| A7.5 | `/analyze` regression | PASS | 浏览器提交 sample inquiry 后 AgentResult、Retrieved Knowledge、Agent Trace 正常展示。 |
| A7.5 | Review regression | PASS | 浏览器详情页提交 review 成功，状态为 `need_clarification`。 |
| A7.5 | Browser console | PASS | `/knowledge`、`/analyze`、review 回归流程 console error count = 0。 |
| A7.5 | Docker Compose | PASS | postgres/backend/frontend healthy，qdrant running。 |

A7.5 继续保持边界：不做知识库上传、在线编辑、删除 chunk、登录权限、Redis、邮件系统、CRM/ERP 或报价系统；不自动报价、不承诺库存、不承诺交期、不自动发送邮件，英文回复草稿必须人工审核。
## A8 Auth & Role-Based Access Test Results

| Priority | Test Case | Result | Notes |
|---|---|---|---|
| A8 | Login API | PASS | `POST /api/auth/login` covered by backend tests. |
| A8 | Current user API | PASS | `GET /api/auth/me` covered by backend tests. |
| A8 | Demo roles | PASS | `admin` / `sales` / `support` demo users are available. |
| A8 | Knowledge admin access | PASS | admin can access `/api/knowledge/status`; sales receives 403 in tests. |
| A8 | Review current user | PASS | authenticated sales review records `sales@example.com`. |
| A8 | Backend pytest | PASS | A8 run: 23 passed. |
| A8 | Frontend build | PASS | A8 run: Next.js build passed. |

A8 仍然是 prototype demo auth，不是完整企业 SSO / OAuth / 多租户账号系统。

## A9 Business Data Adapter Layer Test Results

| Priority | Test Case | Result | Notes |
|---|---|---|---|
| A9 | CSVProductProvider reads products.csv | PASS | Covered by `test_product_providers.py`. |
| A9 | ProductDataProvider list/get/search | PASS | CSV provider returns Product schema objects. |
| A9 | Reserved product provider fallback | PASS | `PRODUCT_PROVIDER=erp` falls back to CSV with clear reason. |
| A9 | ManualInquiryProvider normalize | PASS | Raw dict normalizes to `InquiryInput`. |
| A9 | Website / Email provider skeleton | PASS | Source/channel standardization covered by tests. |
| A9 | `/analyze` regression | PASS | Analyze still returns PLC AgentResult and matched products. |
| A9 | `/login` regression | PASS | Login page and auth API remain available. |
| A9 | `/knowledge` regression | PASS | Admin knowledge status remains available with fallback. |
| A9 | Review regression | PASS | Sales review submission still works. |
| A9 | Auth regression | PASS | Existing auth tests remain passing. |
| A9 | Backend pytest | PASS | A9 run: 33 passed. |
| A9.5 | Frontend build | PASS | Next.js build passed. |
| A9.5 | Docker Compose | PASS | postgres/backend/frontend healthy, qdrant running. |
| A9.5 | Provider smoke check | PASS | CSV list/get/search, Manual normalize, reserved provider fallback verified. |

A9 不接真实 ERP / CRM / 邮箱，不做库存同步、报价系统或自动邮件发送。
A8 仍然是 prototype demo auth，不是完整企业 SSO / OAuth / 多租户账号系统。

## A8.5 Auth & Roles Stabilization Results

| Priority | Test Case | Result | Notes |
|---|---|---|---|
| A8.5 | Docker Compose | PASS | postgres/backend/frontend healthy, qdrant running. |
| A8.5 | `/login` page | PASS | HTTP 200 and screenshot captured as `14_login_page.png`. |
| A8.5 | Admin knowledge access | PASS | admin token can access `/api/knowledge/status`; Qdrant available, points_count = 21. |
| A8.5 | Sales knowledge restriction | PASS | sales token receives 403 for `/api/knowledge/status`; screenshot captured as `15_role_based_knowledge_access.png`. |
| A8.5 | `/analyze` regression | PASS | PLC sample returns AgentResult with product_category = PLC. |
| A8.5 | Review regression | PASS | sales review submitted and recorded as `sales@example.com`. |
| A8.5 | Backend pytest | PASS | 23 passed. |
| A8.5 | Frontend build | PASS | Next.js build passed. |
## A-Final 客服/业务员后台最终集成版

A-Final 已补齐客服/业务员后台闭环：Public Website Inquiry、Email Inquiry Import、Inquiry Console、Requirement Confirmation Card、Candidate Products、Reply Draft edit/copy/export、Human Review、Follow-up Status、Product Library Admin、Knowledge Upload、Qdrant Rebuild Index、Redis basic status integration。

当前边界保持不变：No automatic quotation, no stock commitment, no delivery commitment, no automatic email sending, manual review required。当前产品数据和知识库数据仍为高仿真模拟数据；项目定位仍是 portfolio / prototype 工程化项目，不代表完整生产系统。

## A-Final Customer/Sales Console Test Results

| Priority | Test Case | Result | Notes |
|---|---|---|---|
| A-Final.5 | `/login` | PASS | HTTP 200；admin / sales / support login API 均通过。 |
| A-Final.5 | `/public-inquiry` | PASS | 未登录可提交官网询盘，返回 `channel=website`，生成 inquiry id。 |
| A-Final.5 | `/analyze` Website Inquiry | PASS | 现有 Website Inquiry 分析流程保留。 |
| A-Final.5 | `/analyze` Email Inquiry | PASS | Email Inquiry API 回归通过，VFD sample 返回 AgentResult，matched products = 5。 |
| A-Final.5 | `/inquiries` filters | PASS | API 验证 `channel=email` + `product_category=VFD` 可返回列表。 |
| A-Final.5 | `/inquiries/{id}` detail | PASS | 详情 API 返回 inquiry + agent_result + review_logs。 |
| A-Final.5 | Requirement Confirmation Card | PASS | 前端 build 包含详情页组件；数据来自 AgentResult。 |
| A-Final.5 | Candidate Products | PASS | Email Inquiry 分析返回候选产品。 |
| A-Final.5 | Reply Draft Edit | PASS | 详情页保留可编辑 textarea。 |
| A-Final.5 | Copy Reply | PASS | 前端实现 Clipboard copy，需浏览器手动点击复核。 |
| A-Final.5 | Export Markdown | PASS | 前端实现 Markdown blob download，需浏览器手动点击复核。 |
| A-Final.5 | Human Review | PASS | Review API 返回 `approved`。 |
| A-Final.5 | Follow-up Status | PASS | `PATCH /api/inquiries/{id}/status` 返回 `followed_up`。 |
| A-Final.5 | Product Library | PASS | admin `/api/products` 返回产品；sales 访问返回 403。 |
| A-Final.5 | Knowledge Upload | PASS | 非 `.md` 上传返回失败；`.md` 上传成功。 |
| A-Final.5 | Redis/System Status | PASS | `/api/system/status` 返回 `redis_available=true`。 |
| A-Final.5 | Docker Compose | PASS | postgres/backend/frontend/qdrant/redis 启动；backend/frontend/redis healthy。 |
| A-Final.5 | Backend pytest | PASS | 39 passed。 |
| A-Final.5 | Frontend build | PASS | Next.js build passed，包含 `/public-inquiry` 和 `/products`。 |
| A-Final.5 | Business Boundary | PASS | 文档继续说明不自动报价、不承诺库存、不承诺交期、不自动发送邮件，英文回复草稿必须人工审核。 |

截图说明：自动截图工具需要从外部 npm registry 获取 Playwright CLI，本环境被安全策略拒绝，因此 A-Final 截图 `16_public_inquiry_form.png` 到 `20_knowledge_upload.png` 暂标记为 pending，需要用户手动截图补齐；未伪造截图。

## Final Delivery Test Results

| Priority | Test Case | Result | Notes |
|---|---|---|---|
| Final Delivery | Git status | PASS | `main` 分支，开始时工作区干净。 |
| Final Delivery | Docker Compose config | PASS | 配置包含 frontend/backend/postgres/qdrant/redis。 |
| Final Delivery | Docker Compose up | PASS | 五服务可启动，backend/frontend/postgres/redis healthy，qdrant running。 |
| Final Delivery | Core pages | PASS | `/`、`/login`、`/public-inquiry`、`/analyze`、`/inquiries`、`/knowledge`、`/products` 返回 200。 |
| Final Delivery | Backend health | PASS | `/api/health` 返回 200。 |
| Final Delivery | Swagger | PASS | `/docs` 返回 200。 |
| Final Delivery | Qdrant endpoint | PASS | `http://127.0.0.1:6333` 返回 200。 |
| Final Delivery | Backend pytest | PASS | 39 passed。 |
| Final Delivery | Frontend build | PASS | Next.js build passed。 |
| Final Delivery | Screenshots 16-20 | PENDING | 当前环境无法稳定自动截图，需要用户手动截取真实页面；未伪造截图。 |
| Final Delivery | npm audit known issue | RECORDED | 记录在 `docs/known_issues.md`，本轮不升级依赖。 |
| Final Delivery | Business Boundary | PASS | 继续不自动报价、不承诺库存、不承诺交期、不自动发送邮件，英文回复草稿必须人工审核。 |
