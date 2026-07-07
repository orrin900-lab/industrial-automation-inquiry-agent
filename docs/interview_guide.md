# 面试讲解 Interview Guide

## 1. 30 秒项目介绍

Industrial Automation Inquiry Agent 是一个面向工业自动化外贸场景的 full-stack AI Agent 项目。它帮助客服和业务员处理 PLC、VFD、HMI、工业交换机等产品询盘，把非结构化英文询盘转换为结构化 AgentResult，并提供候选产品、缺失信息、RAG 检索来源、风险提示和英文回复草稿。系统使用 Next.js、FastAPI、PostgreSQL 和 Docker Compose，并保留 Human-in-the-loop 人工审核。

## 2. 2 分钟项目介绍

这个项目从 C+ Streamlit 原型演进到 A 阶段工程化版本。C+ 阶段验证了 Agent workflow、fallback 规则、可选 LLM JSON 抽取、轻量 RAG、Agent Trace 和结构化输出。A 阶段将核心能力封装为 FastAPI，增加 PostgreSQL 持久化、Next.js 前端后台、Docker Compose 一键启动，并补充 README、docs、截图和人工复测报告。

项目重点不是自动客服回复，而是帮助业务员做询盘资格判断和风险控制。系统不会自动报价、不会承诺库存、不会承诺交期，也不会自动发送邮件。英文回复只作为 draft，必须由业务员人工审核。

## 3. 技术架构讲解

- Frontend: Next.js + TypeScript + Tailwind CSS。
- Backend: FastAPI + Pydantic + SQLAlchemy。
- Database: PostgreSQL，开发时保留 SQLite fallback。
- Agent Core: intent classifier、category classifier、requirement extractor、retriever、product matcher、reply draft generator、risk checker。
- RAG: 当前为 lightweight keyword retriever，后续可替换 Qdrant。
- Deployment: Docker Compose 启动 postgres、backend、frontend。

## 4. Agent 工作流讲解

Agent 接收 `InquiryInput` 后，依次执行：

1. Intent Classifier：识别客户意图。
2. Product Category Classifier：判断 PLC / VFD / HMI / Industrial Switch。
3. Requirement Extractor：抽取 brand、model、quantity、technical_specs 等字段。
4. Missing Info Checker：判断缺失信息。
5. Knowledge Retriever：检索 FAQ、selection rules、email templates。
6. Product Matcher：从 `products.csv` 推荐候选产品。
7. Reply Draft Generator：生成英文回复草稿。
8. Risk Checker：检查报价、库存、交期、兼容性等风险。
9. Final AgentResult：返回结构化 JSON。

每一步都会写入 Agent Trace，便于调试和解释。

## 5. 为什么不自动报价

工业自动化产品报价涉及型号、数量、库存、交期、运输、认证、付款条款等多个不确定因素。LLM 或规则系统直接报价会有商业风险，所以当前系统只做 quotation preparation 前的需求确认，不做自动报价。

## 6. 为什么需要 Human-in-the-loop

外贸询盘涉及客户关系和商业承诺。Human-in-the-loop 可以让业务员确认：

- 参数是否完整。
- 候选产品是否合适。
- 回复是否安全。
- 是否需要追问。
- 是否可以进入报价准备。

## 7. 为什么先做 C+ 原型再做 A 阶段工程化

C+ 原型用于快速验证 Agent workflow 是否合理；A 阶段再做 API、数据库、前端、Docker Compose 等工程化能力。这样可以避免一开始就过度工程化，也能保持业务逻辑清晰。

## 8. 当前轻量 RAG 的边界

当前 RAG 使用 Markdown chunk + keyword score，适合 Demo 和原型验证，但不是生产级向量检索。它不能处理复杂语义相似度，也不适合大规模知识库。

## 9. 后续如何升级 Qdrant

A6 建议：

1. 增加 Qdrant Docker 服务。
2. 增加 embedding 层。
3. 将 Markdown chunks 写入 Qdrant。
4. Retriever 支持 Qdrant search。
5. 保留 keyword fallback。
6. 保持 `retrieved_knowledge` 结构不变。

## 10. 这和普通客服机器人有什么区别

普通客服机器人通常偏自然语言对话；这个项目偏业务流程和结构化决策支持。它输出 `AgentResult`，包含参数抽取、缺失信息、候选产品、RAG 来源、Agent Trace、风险提示和人工审核状态，适合沉淀到业务系统中。

## 11. LLM 出错怎么办

系统默认支持 fallback：

- 无 API Key 时使用规则逻辑。
- LLM 返回非法 JSON 时 fallback 到规则抽取。
- Agent Trace 会记录节点 mode。
- 风险检查会阻止报价、库存、交期等不安全承诺。

## 12. 如何生产化

生产化方向：

- Qdrant 替换轻量 RAG。
- Alembic 数据库迁移。
- Redis + async job queue。
- 登录权限和 RBAC。
- CRM/ERP/邮件系统集成。
- 更完整的日志、指标、链路追踪和审计。
- 更大规模真实数据测试。
