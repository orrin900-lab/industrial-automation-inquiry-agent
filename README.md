# Industrial Automation Inquiry Agent

面向工业自动化外贸场景的询盘需求确认与转化辅助 Agent。项目帮助客服 / 外贸业务员处理官网询盘和邮件询盘，完成产品类别判断、需求参数抽取、知识库检索、候选产品推荐、英文回复草稿生成、风险提示与人工审核记录。

当前项目已完成 A-Final 客服/业务员后台最终集成版：`Next.js + FastAPI + Agent Core + PostgreSQL + Qdrant + Redis + Docker Compose + Knowledge Base Admin + Product Library Admin`。项目适合作为 GitHub 作品集、简历项目、面试讲解和 3-5 分钟录屏展示。

## 1. 项目概览 Project Overview

Industrial Automation Inquiry Agent 不是自动成交系统，而是面向 B2B 外贸业务员的内部辅助系统。它将非结构化英文询盘转换为结构化 `AgentResult`，并保留 `Agent Trace` 与 `Retrieved Knowledge`，方便人工复核。

相关文档：

- [系统架构 Architecture](docs/architecture.md)
- [演示脚本 Demo Script](docs/demo_script.md)
- [API 文档 API Overview](docs/api_overview.md)
- [面试讲解 Interview Guide](docs/interview_guide.md)
- [简历描述 Resume Description](docs/resume_description.md)
- [项目总结 Project Summary](docs/project_summary.md)
- [人工复测报告 Manual Test Report](docs/manual_test_report.md)
- [Qdrant RAG 总结 Qdrant RAG Summary](docs/qdrant_rag_summary.md)
- [GitHub 发布指南 GitHub Publish Guide](docs/github_publish_guide.md)
- [录屏演示脚本 Demo Video Script](docs/demo_video_script.md)
- [求职展示材料 Job Ready Package](docs/job_ready_package.md)
- [求职材料包 Career Package](docs/career_package/resume_project_final.md)
  - [面试讲解稿 Interview Pitch](docs/career_package/interview_pitch.md)
  - [技术追问 Q&A](docs/career_package/technical_qa.md)
  - [项目难点与解决方案 Project Challenges](docs/career_package/project_challenges.md)
  - [投递包装说明 Job Application Notes](docs/career_package/job_application_notes.md)
- [A-Final 验收计划 A-Final Acceptance Plan](docs/a_final_acceptance_plan.md)
- [已知事项 Known Issues](docs/known_issues.md)

## 2. 业务场景 Business Scenario

工业自动化外贸询盘经常信息不完整，例如：

- `Need Siemens compatible PLC, 16DI and 8DO, RS485.`
- `Looking for 2.2kW VFD for water pump, 380V three phase.`
- `Need 7 inch HMI with Ethernet and Modbus TCP.`
- `Looking for 8-port gigabit industrial switch, unmanaged is ok.`

业务员需要快速判断：客户想买什么、缺哪些关键参数、有哪些候选产品、应该追问什么，以及英文回复中有哪些风险不能承诺。

## 3. 核心功能 Key Features

- 官网询盘 Website Inquiry 和邮件询盘 Email Inquiry。
- PLC、VFD、HMI、Industrial Switch 四类产品样例。
- 规则 fallback + 可选 LLM JSON 抽取。
- 结构化 `AgentResult`。
- 产品匹配 `Candidate Products`，包含 `match_score`、`match_reason`、`missing_confirmations`。
- Qdrant-based Vector Retrieval + Keyword Fallback。
- `Retrieved Knowledge` 检索来源展示，结构兼容前端。
- `Agent Trace` 可观测性，展示节点 mode、success、latency。
- 风险提示 `Risk Flags`。
- 英文回复草稿 `English Reply Draft`，支持编辑、Copy Reply、Export Markdown，必须人工审核。
- PostgreSQL 持久化 inquiry、AgentResult、AgentRun、AgentStep、ReviewLog。
- 中文 / English UI 切换，使用 `localStorage` 保持语言选择。
- demo 登录与角色权限 `Auth & Role-Based Access`：admin / sales / support。
- 轻量产品库管理 `Product Library Admin`：admin-only demo 产品列表、搜索、新增、启用/停用。
- 轻量知识库运维后台 `Knowledge Base Admin`：查看 Qdrant 状态、chunks 列表、上传 `.md` 并手动重建索引。
- Redis 基础接入：`/api/system/status` 展示 `redis_available`，Redis 不可用时系统不崩溃。
- Docker Compose 一键启动 frontend、backend、postgres、qdrant、redis。

## 4. 系统架构 Architecture

```mermaid
flowchart TD
    U["Sales User / Operator"] --> F["Next.js Frontend"]
    F --> B["FastAPI Backend"]
    B --> S["Agent Service"]
    S --> A["Agent Core"]
    A --> R["Retriever: Qdrant first, keyword fallback"]
    R --> Q[("Qdrant")]
    A --> P["Product Repository"]
    S --> DB[("PostgreSQL")]
```

前端负责业务员工作台展示；后端负责 API、持久化和 Agent 调用；Agent Core 负责意图识别、品类判断、需求抽取、RAG、产品匹配、回复草稿和风险检查；Qdrant 负责知识库向量检索，失败时自动回退到 keyword retriever。

## 5. 技术栈 Tech Stack

- Frontend: Next.js, TypeScript, Tailwind CSS, App Router
- Backend: FastAPI, Pydantic, SQLAlchemy
- Database: PostgreSQL, SQLite fallback
- Vector DB: Qdrant
- Agent Core: rule fallback, optional LLM JSON extraction
- RAG: Markdown loader, heading splitter, hashing embedding, Qdrant retrieval, keyword fallback
- DevOps: Docker Compose, Dockerfile, healthcheck
- Testing: pytest, Next.js build

## 6. Agent 工作流 Agent Workflow

```mermaid
flowchart LR
    I["InquiryInput"] --> C["Intent Classifier"]
    C --> K["Product Category Classifier"]
    K --> E["Requirement Extractor"]
    E --> M["Missing Info Checker"]
    M --> R["Knowledge Retriever"]
    R --> P["Product Matcher"]
    P --> D["Reply Draft Generator"]
    D --> X["Risk Checker"]
    X --> O["Structured AgentResult"]
```

`Knowledge Retriever` 优先使用 Qdrant。若 Qdrant 未启动、collection 未创建或检索失败，会自动使用 keyword fallback，Agent 不会整体失败。

## 7. 数据流 Data Flow

```mermaid
sequenceDiagram
    participant User as Sales User
    participant UI as Next.js Frontend
    participant API as FastAPI Backend
    participant Agent as Agent Core
    participant Q as Qdrant
    participant DB as PostgreSQL

    User->>UI: Submit inquiry
    UI->>API: POST /api/inquiries/analyze
    API->>DB: Save inquiry
    API->>Agent: Run workflow
    Agent->>Q: Retrieve knowledge chunks
    Q-->>Agent: Retrieved Knowledge
    Agent-->>API: AgentResult + Trace
    API->>DB: Save result and steps
    API-->>UI: inquiry_id + agent_result
    User->>UI: Human Review
    UI->>API: POST /api/inquiries/{id}/review
    API->>DB: Save review log
```

## 8. 截图 Screenshots

截图清单见 [docs/screenshots/README.md](docs/screenshots/README.md)。

![Dashboard](docs/screenshots/01_dashboard.png)
![Agent Result](docs/screenshots/03_agent_result.png)
![Inquiry Detail](docs/screenshots/05_inquiry_detail.png)
![Retrieved Knowledge](docs/screenshots/07_retrieved_knowledge.png)
![Agent Trace](docs/screenshots/08_agent_trace.png)
![Swagger API](docs/screenshots/10_swagger_api.png)
![Knowledge Base Admin](docs/screenshots/12_knowledge_base_admin.png)
![Knowledge Reindex Success](docs/screenshots/13_knowledge_reindex_success.png)

## 9. Docker Compose 快速启动 Quick Start

```bash
docker-compose up --build
```

访问地址：

```text
Frontend: http://127.0.0.1:3001
Backend API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs
PostgreSQL: localhost:5432
Qdrant: http://127.0.0.1:6333
Redis: 127.0.0.1:6379
```

构建 Qdrant 知识库索引：

```bash
docker-compose exec backend python scripts/build_qdrant_index.py
```

停止服务：

```bash
docker-compose down
```

清空数据库和 Qdrant volume：

```bash
docker-compose down -v
```

## 10. 本地开发 Local Development

Backend:

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev -- -H 127.0.0.1 -p 3001
```

Backend tests:

```bash
cd backend
PYTHONPATH=. python -m pytest
```

Frontend build:

```bash
cd frontend
npm run build
```

本地 Qdrant URL 可配置为：

```env
QDRANT_URL=http://127.0.0.1:6333
```

## 11. API 概览 API Overview

- `GET /api/health`
- `POST /api/inquiries/analyze`
- `GET /api/inquiries`
- `GET /api/inquiries/{id}`
- `POST /api/inquiries/{id}/review`
- `GET /api/inquiries/samples`
- `GET /api/knowledge/status`
- `GET /api/knowledge/chunks`
- `POST /api/knowledge/reindex`

详细说明见 [docs/api_overview.md](docs/api_overview.md)。

## 12. 演示流程 Demo Workflow

推荐演示流程：

1. 启动 Docker Compose。
2. 执行 Qdrant index build。
3. 打开 `http://127.0.0.1:3001`。
4. 进入 Analyze Inquiry。
5. 加载 PLC 或 VFD sample。
6. 提交分析并展示 AgentResult。
7. 展示 Candidate Products、Missing Information、Retrieved Knowledge、Agent Trace。
8. 进入 Knowledge Base 页面，查看 Qdrant status、chunks 和手动 rebuild index。
9. 进入 Inquiry Detail。
10. 编辑 English Reply Draft。
11. 提交 Human Review。
12. 说明 PostgreSQL 和 Qdrant 持久化。

## 13. 原型边界 Prototype Boundary

当前项目是工程化原型，不是生产销售自动化系统。

- 当前产品数据为高仿真模拟数据。
- 当前 hashing embedding 是 prototype lightweight embedding，不代表最终生产语义 embedding。
- 当前 Qdrant RAG 已具备工程接口，但可继续升级为 OpenAI embeddings 或 sentence-transformers。
- 当前 Knowledge Base Admin 只支持查看状态、查看 chunks 和手动重建索引，不支持上传、编辑或删除知识文档。
- 系统不自动报价。
- 系统不承诺库存。
- 系统不承诺交期。
- 系统不自动发送邮件。
- 英文回复草稿必须由业务员人工审核。
- 登录权限、CRM、ERP、邮件系统、Redis、报价系统尚未接入。
- 当前评估不代表真实生产准确率。

## 14. 路线图 Roadmap

- A7.5 可继续增强 Knowledge Base Admin，例如查看 collection diagnostics 和更细粒度 rebuild 日志。
- 生产级 embedding：OpenAI embeddings 或 sentence-transformers。
- Alembic 数据库迁移。
- Redis 异步任务队列。
- 登录权限与角色控制。
- CRM / ERP / 邮件系统集成。
- 带人工审批接口的报价准备流程。

## 15. 简历亮点 Resume Highlights

- 构建面向 B2B 工业自动化外贸询盘的 full-stack AI Agent 应用。
- 设计结构化 Agent workflow：fallback extraction、Qdrant RAG、product matching、risk checking、Agent Trace。
- 实现 FastAPI API、PostgreSQL 持久化、Next.js 前端后台、Qdrant 向量检索和 Docker Compose 部署。
- 采用 Human-in-the-loop 设计，避免自动报价、库存承诺、交期承诺和自动邮件发送等高风险行为。

英文简历 bullet points 保留在 [docs/resume_description.md](docs/resume_description.md)。
## 16. A8 权限与角色 Auth & Role-Based Access

A8 在现有后台基础上新增轻量 demo 权限系统，让项目更接近企业内部业务后台骨架：

- 新增 `/login` 页面，支持中文 / English 切换。
- 新增 `POST /api/auth/login`、`GET /api/auth/me`、`POST /api/auth/logout`。
- 提供 demo 用户：`admin@example.com / admin123`、`sales@example.com / sales123`、`support@example.com / support123`。
- 前端顶部显示当前用户与角色，并支持退出登录。
- `Knowledge Base Admin` / `/knowledge` 仅 admin 可访问；sales / support 会看到无权限提示。
- Review 提交时如果用户已登录，后端会记录当前登录用户。

边界说明：A8 是 portfolio / prototype 级 demo auth，不是完整企业 SSO / OAuth / 多租户账号系统；没有接入真实企业用户、短信验证码、密码找回或字段级权限。

### A8 Screenshots

![Login Page](docs/screenshots/14_login_page.png)

![Role Based Knowledge Access](docs/screenshots/15_role_based_knowledge_access.png)

## 17. A9 业务数据适配层 Business Data Adapter Layer

A9 将当前模拟数据读取封装为可替换 provider：

- `ProductDataProvider`：产品数据统一接口。
- `CSVProductProvider`：当前默认实现，继续读取 `backend/data/products.csv`。
- `DatabaseProductProvider`：预留给未来 PostgreSQL 产品表，目前不接真实产品库。
- `ERPProductProvider`：预留给未来 SAP / 金蝶 / 用友 / 内部 ERP，目前不接真实 ERP。
- `InquirySourceProvider`：询盘来源统一标准化接口。
- `ManualInquiryProvider`：当前默认实现，保留手动输入询盘。
- `WebsiteInquiryProvider` / `EmailInquiryProvider`：预留真实官网和邮件入口标准化。

当前配置默认：

```env
PRODUCT_PROVIDER=csv
INQUIRY_SOURCE_PROVIDER=manual
```

如果配置为尚未实现的 provider，系统会明确 fallback 到 CSV / Manual，保证 Demo 不崩溃。A9 仍然不接真实 ERP / CRM / 邮箱，不做库存同步、不做报价系统、不自动发送邮件。

## 18. A-Final 客服/业务员后台最终集成版

A-Final 将前期能力整合为一个客服/业务员后台闭环：

- `/public-inquiry`：未登录官网询盘模拟入口，创建 `channel=website` 的 inquiry 记录。
- `/analyze`：支持 Website Inquiry 和 Email Inquiry 手动导入分析。
- `/inquiries`：支持 `channel`、`status`、`product_category` 筛选。
- `/inquiries/{id}`：展示原始询盘、AgentResult、需求确认卡、候选产品、缺失信息、英文回复草稿、Retrieved Knowledge、Agent Trace、Human Review 和 Follow-up Status。
- `Reply Draft`：支持编辑、Copy Reply、Export Markdown；不会自动发送邮件。
- `/products`：admin-only Product Library Admin，支持 demo 产品列表、搜索、新增、启用/停用。
- `/knowledge`：admin-only Knowledge Base Admin，支持 `.md` 上传和手动 Rebuild Qdrant Index。
- `/api/system/status`：显示 Redis availability；Redis 不可用时系统不崩溃。

Docker Compose 当前服务：

- `postgres`
- `backend`
- `frontend`
- `qdrant`
- `redis`

A-Final 仍然保持核心业务边界：No automatic quotation, no stock commitment, no delivery commitment, no automatic email sending, manual review required。当前产品和知识库数据仍为高仿真模拟数据，项目定位仍是 portfolio / prototype 工程化项目。

## 19. Final Delivery 最终交付状态

当前版本已封装为 A 方案最终作品集版本，可用于 GitHub 展示、简历项目、面试讲解和本地录屏演示。

- 稳定分支：`main`
- 稳定 tag：`a-final-customer-sales-console-stable`
- Docker Compose 服务：`frontend` / `backend` / `postgres` / `qdrant` / `redis`
- 后端测试：`39 passed`
- 前端构建：`npm run build` passed
- 核心页面：`/login`、`/public-inquiry`、`/analyze`、`/inquiries`、`/knowledge`、`/products`
- 最终封版说明：见 [A-Final Acceptance Plan](docs/a_final_acceptance_plan.md) 和 [Manual Test Report](docs/manual_test_report.md)
- 已知事项：见 [Known Issues](docs/known_issues.md)

A-Final pending screenshots `16_public_inquiry_form.png` 到 `20_knowledge_upload.png` 需要在本地页面运行时手动截取真实截图；README 仅引用已经存在的真实截图，不引用 pending 图片。
