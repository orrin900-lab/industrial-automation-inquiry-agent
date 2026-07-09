# 最终简历项目描述 Resume Project Final

项目名称：Industrial Automation Inquiry Agent  
中文名称：工业自动化外贸询盘分析与转化辅助 AI Agent

定位：AI Agent 应用开发 / 大模型应用开发 / RAG 应用开发 / Full-stack AI Application。  
说明：该项目是作品集级 prototype 工程化项目，使用高仿真模拟数据，不代表真实企业生产上线；系统不自动报价、不承诺库存、不承诺交期、不自动发送邮件。

## 1. 中文简短版：2-3 行

基于 FastAPI、Next.js、PostgreSQL、Qdrant、RAG 和 Docker Compose，构建工业自动化外贸询盘分析 AI Agent，支持 PLC、VFD、HMI、工业交换机等询盘的结构化需求抽取、知识库检索、候选产品推荐、Agent Trace 和 Human-in-the-loop 人工审核。

项目面向 Industrial Automation + Export Sales 场景，体现从行业业务理解到 AI Agent 工程落地的迁移能力，包含 Keyword Fallback、Bilingual UI 和轻量 Knowledge Base Admin。

## 2. 中文标准版：5-6 行

设计并实现一个面向工业自动化外贸询盘场景的 full-stack AI Agent prototype，帮助业务员将非结构化英文询盘转换为结构化 `AgentResult`。  
后端使用 FastAPI、Pydantic、SQLAlchemy 封装 Agent Workflow，并通过 PostgreSQL 持久化 inquiry、AgentResult、AgentStep 和 ReviewLog。  
RAG 层使用 Qdrant 存储 Markdown 知识库 chunks，支持 deterministic hashing embedding，并保留 Keyword Fallback，保证 Qdrant 不可用时系统仍可演示。  
前端使用 Next.js、TypeScript、Tailwind CSS 构建业务员后台，展示 Candidate Products、Retrieved Knowledge、Agent Trace、Human Review 和 Bilingual UI。  
使用 Docker Compose 编排 PostgreSQL、Qdrant、FastAPI backend 和 Next.js frontend，并补充 Knowledge Base Admin 用于查看 collection 状态、chunks 和手动 rebuild index。  
项目明确遵守业务风险边界：不自动报价、不承诺库存、不承诺交期、不自动发送邮件，所有英文回复草稿必须人工审核。

## 3. 中文详细版：8-10 行

本项目是一个面向 Industrial Automation Export Sales 场景的 AI Agent 应用，模拟业务员处理官网询盘和邮件询盘的需求确认流程。  
系统支持 PLC、VFD、HMI、Industrial Switch 四类工业产品，能够识别客户意图、判断产品类别、抽取品牌、型号、数量和关键技术参数，并给出缺失信息和追问问题。  
后端采用 FastAPI 封装 Agent Core，使用 Pydantic 保证输入输出结构化，使用 PostgreSQL 保存询盘、AgentResult、AgentRun、AgentStep 和 ReviewLog。  
Agent Workflow 保留规则 fallback 和可选 LLM JSON extraction，无 API Key 时仍可运行，适合作品集演示和本地复测。  
RAG 层从 Markdown 知识库加载 FAQ、选型规则和邮件模板，切分 chunks 后写入 Qdrant，并通过 deterministic hashing embedding 实现本地无外部依赖的向量检索。  
当 Qdrant 不可用时，Retriever 自动 fallback 到 Keyword Retriever，保证 Agent 不因向量库异常整体失败。  
前端使用 Next.js App Router、TypeScript 和 Tailwind CSS，实现 Dashboard、Analyze、Inquiry List、Inquiry Detail、Human Review、Bilingual UI 和 Knowledge Base Admin。  
Knowledge Base Admin 支持查看 Qdrant collection 状态、points_count、chunks 列表、source_file 筛选和手动 Rebuild Qdrant Index。  
项目使用 Docker Compose 一键启动 frontend、backend、PostgreSQL 和 Qdrant，并通过 pytest、frontend build、manual test report 和真实截图完成稳定收口。  
项目严格控制业务边界，不自动报价、不承诺库存、不承诺交期、不自动发送邮件，英文回复草稿必须由业务员人工审核。

## 4. 中文简历 Bullet Points：5-8 条

- 构建工业自动化外贸询盘 AI Agent prototype，覆盖 Industrial Automation / Export Sales 场景下 PLC、VFD、HMI、Industrial Switch 的需求确认流程。
- 使用 FastAPI + Pydantic 设计结构化 Agent API，输出 `AgentResult`，包含需求抽取、缺失信息、候选产品、英文回复草稿、风险提示、Retrieved Knowledge 和 Agent Trace。
- 使用 PostgreSQL 持久化 inquiry、AgentResult、AgentRun、AgentStep、ReviewLog，支持询盘列表、详情和 Human-in-the-loop 人工审核。
- 使用 Qdrant 构建 RAG 检索链路，将 Markdown FAQ、选型规则、邮件模板切分为 chunks 并写入向量库，支持 Keyword Fallback。
- 设计 deterministic hashing embedding，保证无 API Key、无外部模型下载时也能完成本地可运行的 prototype vector retrieval。
- 使用 Next.js + TypeScript + Tailwind CSS 实现业务员后台，包含 Dashboard、Analyze、Inquiry Detail、Bilingual UI 和 Knowledge Base Admin。
- 使用 Docker Compose 编排 FastAPI backend、Next.js frontend、PostgreSQL 和 Qdrant，完成一键启动、健康检查和端到端复测。
- 坚持业务风险边界：系统只辅助需求确认和回复草稿生成，不自动报价、不承诺库存/交期、不自动发送邮件。

## 5. English Short Version

Built an AI-powered inquiry qualification agent for industrial automation export sales using FastAPI, Next.js, PostgreSQL, Qdrant RAG, and Docker Compose. The system converts unstructured English inquiries into structured AgentResult outputs, with candidate product matching, retrieved knowledge, agent trace observability, and human-in-the-loop review.

## 6. English Standard Version

Designed and implemented a full-stack AI Agent prototype for industrial automation export sales inquiries.  
The backend uses FastAPI, Pydantic, SQLAlchemy, and PostgreSQL to persist inquiries, agent results, execution steps, and human review logs.  
The RAG layer uses Qdrant with deterministic hashing embeddings and keyword fallback to retrieve FAQ, selection rules, and email templates.  
The frontend is built with Next.js, TypeScript, and Tailwind CSS, providing dashboard, inquiry analysis, inquiry detail, bilingual UI, and Knowledge Base Admin pages.  
The system is packaged with Docker Compose and explicitly follows business boundaries: no automatic quotation, no stock or lead-time promises, and no automatic email sending.

## 7. English Bullet Points

- Built a full-stack AI Agent prototype for Industrial Automation Export Sales using FastAPI, Next.js, PostgreSQL, Qdrant, RAG, and Docker Compose.
- Designed a structured Agent Workflow for intent classification, product category detection, requirement extraction, missing-info checking, RAG retrieval, product matching, reply drafting, and risk checking.
- Implemented Qdrant-based vector retrieval with deterministic hashing embedding and Keyword Fallback to keep the demo runnable without external API keys.
- Persisted inquiries, AgentResult, AgentStep, AgentRun, and Human Review logs in PostgreSQL.
- Developed a bilingual Next.js dashboard for inquiry analysis, candidate products, Retrieved Knowledge, Agent Trace, and Human-in-the-loop review.
- Added a lightweight Knowledge Base Admin to inspect Qdrant status, chunks, source_file filters, and manually rebuild the RAG index.
- Maintained business safety boundaries: no automatic pricing, no stock/lead-time promises, and no automatic email sending.

## 8. A-Final 最终版补充

A-Final 将项目从“询盘分析后台”补齐为客服 / 外贸业务员可演示的完整后台闭环：

- Public Inquiry：`/public-inquiry` 支持未登录官网询盘模拟入口。
- Email Inquiry Import：`/analyze` 支持邮件标题、发件人、公司、国家和邮件正文手动导入。
- Auth & Role-Based Access：`admin`、`sales`、`support` demo 角色，admin 可访问 Product Library Admin 和 Knowledge Base Admin。
- Product Library Admin：`/products` 支持 demo 产品库列表、搜索、新增和启用 / 停用。
- Knowledge Upload：`/knowledge` 支持 `.md` 知识文件上传和手动 Rebuild Qdrant Index。
- Reply Draft Workspace：英文回复草稿支持编辑、Copy Reply、Export Markdown。
- Follow-up Status：详情页可标记跟进状态。
- Redis / System Status：Docker Compose 增加 Redis，`/api/system/status` 展示系统状态。

简历表达时建议写成“portfolio / prototype 工程化项目”，不要写成真实生产上线、真实企业数据接入、自动报价或自动发邮件系统。

### A-Final 中文简历 bullet points

- 构建工业自动化外贸询盘客服 / 业务员后台，覆盖 Public Inquiry、Email Inquiry Import、Inquiry Console、Human Review、Follow-up Status、Product Library Admin 和 Knowledge Base Admin。
- 使用 FastAPI + PostgreSQL 保存询盘、AgentResult、Agent Trace、ReviewLog 和跟进状态，并通过 Next.js 展示结构化分析结果。
- 使用 Qdrant RAG + Keyword Fallback 检索 FAQ、选型规则和邮件模板，保留 Retrieved Knowledge 可解释来源。
- 通过 Auth & Role-Based Access 区分 admin / sales / support，限制知识库与产品库管理入口。
- 使用 Docker Compose 编排 frontend、backend、postgres、qdrant、redis，完成本地一键启动与验收。

### A-Final English resume bullets

- Built a customer/sales inquiry console for industrial automation export sales, covering public website inquiries, manual email inquiry import, inquiry analysis, human review, follow-up status, product library admin, and knowledge base admin.
- Implemented FastAPI APIs with PostgreSQL persistence for inquiries, structured AgentResult, Agent Trace, review logs, and follow-up status.
- Integrated Qdrant-based RAG with keyword fallback to retrieve FAQ, selection rules, and email templates while keeping Retrieved Knowledge explainable.
- Added demo role-based access control for admin, sales, and support users, restricting product and knowledge admin pages to admin users.
- Packaged the system with Docker Compose across Next.js frontend, FastAPI backend, PostgreSQL, Qdrant, and Redis.
