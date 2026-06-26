# Resume Description

## 中文项目描述

工业自动化外贸询盘需求确认与转化辅助 Agent。项目面向 PLC、变频器、HMI、工业交换机等工业自动化产品的 B2B 外贸询盘场景，构建了从客户原始询盘输入、Agent 结构化分析、产品候选推荐、知识库检索、英文回复草稿生成，到业务员人工审核的完整闭环。系统采用 Next.js + FastAPI + PostgreSQL + Docker Compose 架构，支持规则 fallback、可选 LLM JSON 抽取、轻量 RAG、Agent Trace 可观测性和 Human-in-the-loop 风险控制。

## English Project Description

Built a full-stack AI Agent application for industrial automation export inquiry qualification. The system supports PLC, VFD, HMI, and Industrial Switch inquiries, extracts structured requirements, retrieves knowledge sources, recommends candidate products, generates an English reply draft, records Agent execution traces, and persists human review decisions. The project uses Next.js, FastAPI, PostgreSQL, Docker Compose, lightweight RAG, rule-based fallback, and optional LLM JSON extraction.

## 中文简历 Bullet Points

- 设计并实现工业自动化外贸询盘辅助 Agent，支持 PLC、变频器、HMI、工业交换机四类产品需求识别与结构化抽取。
- 使用 FastAPI 封装 Agent Core，基于 Pydantic 定义 `InquiryInput`、`AgentResult`、`ProductCandidate` 等结构化 Schema。
- 实现规则 fallback + 可选 LLM JSON 抽取机制，保证无 API Key 场景下 Demo 仍可稳定运行。
- 构建轻量 RAG 检索链路，支持 Markdown 知识库加载、chunk metadata、检索来源展示。
- 设计 Agent Execution Trace，可展示每个节点的模式、耗时、输出摘要和 fallback 情况。
- 使用 SQLAlchemy + PostgreSQL 持久化 inquiry、agent_result、agent_run、agent_step、review_log。
- 使用 Next.js + TypeScript + Tailwind CSS 构建客服/业务员后台，支持询盘分析、列表、详情、英文草稿编辑和人工审核。
- 使用 Docker Compose 编排 PostgreSQL、FastAPI、Next.js，实现一键启动和数据 volume 持久化。
- 在业务边界上坚持 Human-in-the-loop，不自动报价、不承诺库存、不承诺交期、不自动发送邮件。

## English Resume Bullet Points

- Built a full-stack AI Agent platform for B2B industrial automation export inquiry qualification.
- Designed a structured Agent workflow for intent classification, category detection, requirement extraction, RAG retrieval, product matching, reply drafting, and risk checking.
- Implemented FastAPI APIs with Pydantic schemas and SQLAlchemy persistence for inquiries, AgentResult, AgentRun, AgentStep, and ReviewLog records.
- Built a Next.js sales console for inquiry analysis, AgentResult visualization, retrieved knowledge display, Agent Trace inspection, and human review.
- Implemented rule-based fallback and optional LLM JSON extraction to keep the demo reliable without API keys.
- Added lightweight RAG over Markdown knowledge files with source metadata and retrieval previews.
- Containerized PostgreSQL, FastAPI, and Next.js using Docker Compose with health checks and persistent volumes.
- Applied human-in-the-loop safety boundaries to avoid automatic quotation, stock promises, lead time promises, and auto email sending.

## Technical Keywords

- AI Agent
- LangGraph-style workflow
- FastAPI
- Next.js
- TypeScript
- Tailwind CSS
- PostgreSQL
- SQLAlchemy
- Docker Compose
- Pydantic
- RAG
- Human-in-the-loop
- Agent Trace
- Structured JSON Output
- Rule Fallback
- B2B Export Sales
- Industrial Automation

## Interview Highlights

- Strong scenario fit: B2B industrial automation export inquiries are technical, incomplete, and risk-sensitive.
- Clear engineering evolution: C+ prototype first, then FastAPI, persistence, frontend, Docker Compose.
- Reliable demo design: fallback rules make the app runnable without LLM API keys.
- Traceability: Agent steps and retrieved knowledge are visible to users.
- Safety: manual review is built into the product flow instead of added as an afterthought.
