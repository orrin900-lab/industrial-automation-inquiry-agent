# 简历描述 Resume Description

## 中文项目描述

Industrial Automation Inquiry Agent 是一个面向工业自动化外贸询盘的 full-stack AI Agent 项目，覆盖 PLC、VFD、HMI、Industrial Switch 等产品场景。系统可以将客户英文询盘转化为结构化 `AgentResult`，完成需求抽取、缺失信息判断、Qdrant RAG 检索、候选产品推荐、风险提示、英文回复草稿生成和 Human-in-the-loop 人工审核。

项目采用 `Next.js + FastAPI + PostgreSQL + Qdrant + Docker Compose` 架构，保留无 API Key 可运行的 rule fallback 和 Qdrant 不可用时的 keyword fallback。当前使用高仿真模拟数据，不自动报价、不承诺库存、不承诺交期、不自动发送邮件。

## English Project Description

Industrial Automation Inquiry Agent is a full-stack AI Agent prototype for B2B industrial automation export inquiry qualification. It converts raw English inquiries into structured `AgentResult`, extracts technical requirements, retrieves knowledge from Qdrant RAG, recommends candidate products, generates English reply drafts, records Agent Trace, and supports human review.

The project uses Next.js, FastAPI, PostgreSQL, Qdrant, Docker Compose, rule-based fallback, optional LLM JSON extraction, and keyword fallback when Qdrant is unavailable. It is a portfolio-grade engineering prototype based on synthetic demo data, not an automatic quotation or email-sending system.

## 简短版 2-3 行

工业自动化外贸询盘 AI Agent，基于 Next.js + FastAPI + PostgreSQL + Qdrant + Docker Compose 构建。系统支持结构化需求抽取、Qdrant RAG 检索、候选产品推荐、Agent Trace 可观测性和 Human-in-the-loop 人工审核。

Full-stack AI Agent for industrial automation export inquiry qualification, featuring structured AgentResult, Qdrant RAG, keyword fallback, PostgreSQL persistence, bilingual UI, and Docker Compose deployment.

## 标准版 5-6 行

- 设计并实现工业自动化外贸询盘辅助 Agent，支持 PLC、VFD、HMI、Industrial Switch 四类产品需求识别与结构化抽取。
- 使用 FastAPI 封装 Agent Core，基于 Pydantic 输出结构化 `AgentResult`，并通过 SQLAlchemy + PostgreSQL 持久化 inquiry、AgentResult、AgentRun、AgentStep 和 ReviewLog。
- 使用 Qdrant 构建 knowledge retrieval 链路，将 Markdown 知识库切 chunk 后写入 vector collection，并保留 keyword fallback。
- 使用 Next.js + TypeScript + Tailwind CSS 构建客服 / 外贸业务员后台，支持询盘分析、详情查看、Retrieved Knowledge、Agent Trace 和 Human Review。
- 使用 Docker Compose 编排 frontend、backend、PostgreSQL、Qdrant，实现本地一键启动和完整演示链路。
- 系统坚持 Human-in-the-loop，不自动报价、不承诺库存、不承诺交期、不自动发送邮件。

## 面试展开版 10 行左右

1. 项目面向 B2B 工业自动化外贸场景，解决英文询盘信息不完整、产品参数复杂、回复风险高的问题。
2. Agent workflow 包含 intent classification、product category classification、requirement extraction、missing info check、RAG retrieval、product matching、reply draft generation、risk check。
3. 后端使用 FastAPI + Pydantic，API 返回结构化 JSON，而不是只返回自然语言文本。
4. 数据层使用 PostgreSQL 保存 inquiry、AgentResult、AgentRun、AgentStep 和 ReviewLog，并保留 SQLite fallback 方便本地开发。
5. RAG 从 lightweight keyword-based retrieval 升级为 Qdrant-based vector retrieval + keyword fallback。
6. 当前 embedding 使用 deterministic hashing embedding，384 维、本地运行、无 API Key、无外部模型下载，定位为 prototype lightweight embedding。
7. Qdrant 不可用时自动 fallback 到 keyword retriever，保证 demo 和基础业务链路不会因为向量库故障整体失败。
8. 前端使用 Next.js + TypeScript + Tailwind CSS，展示 AgentResult、Candidate Products、Retrieved Knowledge、Agent Trace、Risk Flags 和 Human Review。
9. 项目使用 Docker Compose 一键启动 PostgreSQL、Qdrant、FastAPI backend 和 Next.js frontend。
10. 项目强调 Human-in-the-loop 和风险边界，不自动报价、不承诺库存、不承诺交期、不自动发送邮件。

## English Resume Bullet Points

- Built a full-stack AI Agent prototype for B2B industrial automation export inquiry qualification.
- Designed an Agent workflow covering intent classification, category detection, requirement extraction, RAG retrieval, product matching, reply drafting, risk checking, and human review.
- Implemented FastAPI APIs with Pydantic schemas and SQLAlchemy persistence for inquiries, AgentResult, AgentRun, AgentStep, and ReviewLog.
- Integrated Qdrant-based vector retrieval over Markdown knowledge chunks with deterministic hashing embeddings and keyword fallback.
- Built a Next.js sales console for inquiry analysis, structured AgentResult visualization, Retrieved Knowledge display, Agent Trace inspection, and human review submission.
- Containerized PostgreSQL, Qdrant, FastAPI, and Next.js with Docker Compose health checks and persistent volumes.
- Added bilingual UI support and portfolio-ready documentation for GitHub, resume, interview walkthrough, and demo recording.
- Applied Human-in-the-loop safety boundaries to avoid automatic quotation, stock promises, lead time promises, and automatic email sending.

## 技术关键词 Technical Keywords

- FastAPI
- Next.js
- TypeScript
- Tailwind CSS
- PostgreSQL
- SQLAlchemy
- Docker Compose
- Qdrant
- RAG
- Agent Workflow
- Human-in-the-loop
- Keyword Fallback
- Agent Trace
- Structured AgentResult
- Pydantic
- i18n / bilingual UI
- B2B Export Sales
- Industrial Automation

## 面试时可以强调的亮点

- 场景明确：工业自动化外贸询盘是技术参数密集、信息不完整且风险敏感的真实 B2B 场景。
- 工程完整：前端、后端、数据库、向量库、Docker Compose、测试、文档、截图和演示脚本都已覆盖。
- 可观测：Agent Trace 展示每个节点的 mode、success、latency 和 output_summary。
- 可降级：LLM 无 API Key 时规则 fallback；Qdrant 不可用时 keyword fallback。
- 风险控制：系统只做询盘资格确认和回复草稿，不做自动报价、库存承诺、交期承诺或自动邮件发送。
- 可演进：当前 hashing embedding 可平滑升级到 OpenAI embeddings、sentence-transformers 或 bge 系列模型。
