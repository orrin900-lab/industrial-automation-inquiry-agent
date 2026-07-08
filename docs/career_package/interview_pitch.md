# 面试讲解稿 Interview Pitch

适用方向：AI Agent 应用开发、大模型应用开发、RAG 应用开发、Python 后端、Full-stack AI Application。  
项目定位：作品集 / prototype 工程化项目，不是完整生产系统，不使用真实企业数据，不自动报价、不承诺库存、不自动发送邮件。

## 1. 30 秒版

我做了一个面向工业自动化外贸询盘的 AI Agent 项目。业务员收到英文询盘后，系统可以识别客户意图、判断产品类别、抽取技术参数、找出缺失信息，并结合 Qdrant RAG 检索 FAQ、选型规则和邮件模板，生成候选产品、风险提示和英文回复草稿。  

技术上，后端是 FastAPI + PostgreSQL + Qdrant，前端是 Next.js + TypeScript，使用 Docker Compose 一键启动。项目还做了 Agent Trace、Human-in-the-loop 人工审核、Keyword Fallback、Bilingual UI 和 Knowledge Base Admin。它是一个工程化 prototype，重点展示我把工业自动化业务理解迁移到 AI Agent 应用开发的能力。

## 2. 1 分钟版

这个项目叫 Industrial Automation Inquiry Agent，是一个面向工业自动化外贸场景的询盘分析 Agent。这个场景和我的行业背景比较贴近，因为工业品询盘经常不是简单问答，而是要判断 PLC、变频器、HMI、工业交换机等产品类别，确认型号、数量、供电、通信协议、I/O 点数等参数。

系统的目标不是自动成交，而是帮助业务员做需求确认和转化辅助。用户提交官网或邮件询盘后，后端 Agent Workflow 会完成意图识别、品类判断、参数抽取、缺失信息判断、RAG 检索、候选产品匹配、英文回复草稿和风险检查。所有结果都会结构化为 `AgentResult`，前端用 Next.js 展示 Candidate Products、Retrieved Knowledge、Agent Trace 和 Human Review。

工程上，我用了 FastAPI、PostgreSQL、Qdrant、Docker Compose 和 Next.js。Qdrant 用来保存 Markdown 知识库 chunks，保留 Keyword Fallback，Qdrant 不可用时系统仍能运行。项目明确不自动报价、不承诺库存和交期、不自动发送邮件，英文回复草稿必须人工审核。

## 3. 3 分钟版

这个项目的业务背景是工业自动化外贸询盘。传统客服机器人更偏对话，但工业品询盘需要做技术参数确认和风险控制。比如客户说需要 Siemens compatible PLC with 16DI and 8DO，业务员不仅要识别这是 PLC，还要确认输出类型、电源、通信接口、数量、应用场景，以及有没有不能承诺的库存、交期或兼容性风险。

所以我把项目设计成一个 Human-in-the-loop 的 AI Agent，而不是自动销售系统。Agent Workflow 包含 intent classifier、product category classifier、requirement extractor、missing info checker、knowledge retriever、product matcher、reply draft generator 和 risk checker。每一步都有结构化输出，最终返回 `AgentResult`，并记录 `Agent Trace`，方便解释系统为什么这么判断。

后端使用 FastAPI 封装 API，Pydantic 保证输入输出结构，PostgreSQL 保存 inquiry、AgentResult、AgentStep 和 ReviewLog。前端使用 Next.js、TypeScript 和 Tailwind CSS，提供 Dashboard、Analyze、Inquiry List、Inquiry Detail、Human Review 和 Bilingual UI。业务员可以查看候选产品、缺失信息、RAG 来源和英文回复草稿，再人工提交审核状态。

RAG 部分是项目的重点之一。我先从 Markdown 知识库加载 FAQ、选型规则和邮件模板，按 heading 切 chunk，然后使用 deterministic hashing embedding 写入 Qdrant。这个 embedding 不是生产级语义模型，但好处是无 API Key、无模型下载依赖，适合 prototype 稳定演示。Qdrant 不可用时，Retriever 会 fallback 到 keyword retriever，保证 Agent 链路不会整体失败。

A7 还增加了 Knowledge Base Admin，能查看 Qdrant collection、points_count、chunks 列表、source_file 筛选，并手动 rebuild index。这个页面不是完整 CMS，不支持上传、编辑和删除，主要用于展示 RAG 运维可观测性。

整个项目用 Docker Compose 编排 frontend、backend、PostgreSQL 和 Qdrant，并有 pytest、frontend build、manual test report 和截图。它不是完整生产系统，但展示了我从业务场景、Agent Workflow、RAG、后端持久化、前端展示、Docker 部署到风险边界控制的一整套工程思考。

## 4. 5 分钟版

如果有 5 分钟，我会按业务闭环讲这个项目。

第一，业务背景。工业自动化外贸询盘通常信息不完整，客户可能只说需要 PLC、VFD、HMI 或 Industrial Switch，但缺少关键参数。真实业务里，业务员不能直接报价或承诺库存交期，必须先确认需求。

第二，项目目标。我做的不是普通聊天机器人，而是 Inquiry Qualification Agent。它把原始英文询盘转成结构化 `AgentResult`，帮助业务员看清客户意图、产品类别、技术参数、缺失字段、候选产品、知识库来源、回复草稿和风险提示。

第三，系统架构。前端是 Next.js + TypeScript + Tailwind CSS，后端是 FastAPI + Pydantic + SQLAlchemy，数据库是 PostgreSQL，RAG 使用 Qdrant，整体用 Docker Compose 启动。前端只负责展示和人工审核，核心逻辑在后端 Agent Core。

第四，Agent Workflow。流程包括意图识别、品类判断、需求抽取、缺失信息检查、RAG 检索、候选产品匹配、回复草稿生成和风险检查。每个节点写入 Agent Trace，最终输出结构化 JSON。无 LLM API Key 时使用规则 fallback，保证 demo 可运行。

第五，RAG / Qdrant。知识库来自 Markdown 文件：FAQ、selection rules 和 email templates。系统切分 chunks，使用 deterministic hashing embedding 写入 Qdrant。当前 embedding 是 prototype 方案，后续可以替换为 OpenAI embeddings、sentence-transformers 或 bge 系列模型。Qdrant 不可用时 fallback 到 keyword retrieval。

第六，Human Review。系统只生成英文回复草稿，不自动发送邮件。Review Form 只保存审核状态、编辑后的草稿和备注。这个设计体现了工业品外贸的风险控制：不自动报价、不承诺库存、不承诺交期。

第七，Knowledge Base Admin。A7 增加了 `/knowledge` 页面，能查看 Qdrant 状态、points_count、chunks、source_file 筛选并手动 rebuild index。这说明我不只是做了一个调用 RAG 的黑盒，也考虑了知识库运维和可观测性。

第八，测试与边界。后端 pytest 通过，前端 build 通过，Docker Compose 已验证，浏览器复测覆盖 `/knowledge`、`/analyze` 和 review。边界上，我会明确说明项目使用模拟数据，是 portfolio / prototype，不是完整生产系统。

## 5. 面试官追问时的展开顺序

建议按下面顺序回答，避免一上来陷入技术细节：

1. 业务背景：工业自动化询盘为什么复杂。
2. 项目目标：不是聊天机器人，而是需求确认和转化辅助 Agent。
3. Agent Workflow：每个节点做什么，为什么结构化输出。
4. RAG / Qdrant：知识库如何切 chunk、写入和检索。
5. Fallback：无 LLM / 无 Qdrant 时如何保证可运行。
6. 可观测性：Agent Trace、Retrieved Knowledge、Knowledge Base Admin。
7. Human Review：为什么不自动报价、不自动发送邮件。
8. 工程化：FastAPI、PostgreSQL、Next.js、Docker Compose、pytest。
9. 边界：模拟数据、prototype、不是生产系统。
10. 后续升级：生产级 embedding、权限、知识库上传、邮件/CRM/ERP 集成。

