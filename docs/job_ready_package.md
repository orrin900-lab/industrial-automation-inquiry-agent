# 求职展示材料 Job Ready Package

## 1. 简历项目名称建议

中文：

```text
工业自动化外贸询盘分析与转化辅助 AI Agent
```

英文：

```text
Industrial Automation Inquiry Agent
```

## 2. 简历项目描述短版

基于 FastAPI、Next.js、PostgreSQL、Qdrant 和 Docker Compose 构建工业自动化外贸询盘 AI Agent，支持结构化需求抽取、RAG 检索、候选产品推荐、Agent Trace 和 Human-in-the-loop 人工审核。

## 3. 简历项目描述标准版

设计并实现一个面向工业自动化外贸场景的 full-stack AI Agent 系统，覆盖 PLC、VFD、HMI、Industrial Switch 等产品询盘。系统使用 FastAPI 封装 Agent Workflow，使用 PostgreSQL 持久化询盘、AgentResult、AgentStep 和 ReviewLog，使用 Qdrant 构建 RAG 检索链路，并通过 Next.js 前端展示结构化结果、Retrieved Knowledge、Agent Trace 和 Human Review。项目使用 Docker Compose 一键启动，并保留 LLM fallback 与 Keyword Fallback，保证无 API Key 或 Qdrant 不可用时仍可演示。

## 4. 面试 1 分钟介绍

这个项目是一个面向工业自动化外贸询盘的 AI Agent。业务员经常收到英文询盘，但客户信息不完整，比如只说需要 PLC、VFD 或 HMI，却缺少数量、输出类型、通讯协议等关键参数。我的系统会把原始询盘转成结构化 AgentResult，抽取需求、判断缺失信息、从产品库推荐候选产品，并通过 Qdrant RAG 检索 FAQ、选型规则和邮件模板。前端用 Next.js 展示 AgentResult、Retrieved Knowledge、Agent Trace 和人工审核表单，后端用 FastAPI、PostgreSQL 和 Docker Compose。系统不自动报价、不承诺库存、不自动发邮件，所有英文回复都必须人工审核。

## 5. 面试 3 分钟介绍

项目从 C+ 原型开始，先用 Streamlit 验证 Agent Workflow 和结构化输出，然后进入 A 阶段工程化。A 阶段先用 FastAPI 封装 Agent Core，再加 PostgreSQL 持久化，然后做 Next.js 前端后台，最后用 Docker Compose 编排 PostgreSQL、Qdrant、backend 和 frontend。

Agent Workflow 包括意图识别、产品类别判断、需求抽取、缺失信息判断、RAG 检索、候选产品匹配、英文回复草稿生成和风险检查。A6 中我把原来的 lightweight keyword RAG 升级成 Qdrant-based Vector Retrieval + Keyword Fallback。当前 embedding 是 deterministic hashing embedding，384 维、本地运行、无 API Key、无外部模型下载，适合 prototype 演示。后续可以替换成 OpenAI embeddings、sentence-transformers 或 bge 系列模型。

这个项目的重点不是“自动成交”，而是 Human-in-the-loop 的业务辅助。系统会生成英文回复草稿，但不会自动发送邮件；会提醒业务员不要报价、不要承诺库存和交期。这样更符合工业品外贸场景的风险控制要求。

## 6. 面试技术亮点讲法

- FastAPI：封装 Agent Core，提供 `/api/inquiries/analyze`、列表、详情、review 等 API。
- Next.js：构建业务员后台，支持 bilingual UI、结构化结果展示和人工审核。
- PostgreSQL：持久化 inquiry、AgentResult、AgentRun、AgentStep、ReviewLog。
- Qdrant：保存知识库 chunks 的向量索引，支持 RAG 检索。
- RAG：Markdown loader、heading splitter、hashing embedding、Qdrant retrieval、Keyword Fallback。
- Agent Workflow：每个节点输出结构化结果，并写入 Agent Trace。
- Docker Compose：一键启动 PostgreSQL、Qdrant、FastAPI backend、Next.js frontend。
- Human-in-the-loop：回复草稿必须人工审核，避免自动报价和自动发送邮件。

## 7. 面试业务价值讲法

- 提高业务员处理技术询盘的速度。
- 把非结构化英文询盘转成结构化字段，便于后续 CRM/ERP 集成。
- 帮助业务员发现缺失参数，减少反复沟通。
- 推荐候选产品，但不替代人工确认。
- 将知识库来源和 Agent Trace 可视化，提高可解释性。
- 通过 Human Review 降低报价、库存、交期承诺风险。

## 8. 项目难点与解决方案

| 难点 | 解决方案 |
| --- | --- |
| 无 LLM API Key 时如何演示 | 保留 rule fallback，保证 demo 可运行。 |
| Qdrant 不可用时如何避免整体失败 | 保留 Keyword Fallback，并在 Agent Trace 中记录 `keyword_fallback`。 |
| 如何避免模型凭空推荐产品 | 候选产品必须来自 `products.csv` 和 ProductRepository。 |
| 如何解释 Agent 过程 | 保存 Agent Trace，展示 step_name、mode、latency、output_summary。 |
| 如何控制业务风险 | 不自动报价、不承诺库存、不承诺交期、不自动发送邮件，回复草稿必须人工审核。 |
| 如何保持前端兼容 | `retrieved_knowledge` 结构不变，前端无需大改。 |

## 9. 可被追问的问题和回答

### Q1：为什么不用纯 LLM 直接回答？

因为工业自动化询盘涉及型号、参数、数量、库存、交期和商务风险。纯自然语言回答不够可控，所以我把输出设计成结构化 `AgentResult`，并加入产品库、RAG、Risk Checker 和 Human Review。

### Q2：Qdrant 在项目里解决什么问题？

Qdrant 用于知识库向量检索，把 FAQ、选型规则和邮件模板切成 chunks 后写入 collection。Agent 分析询盘时检索相关知识来源，返回到 `Retrieved Knowledge`，增强可解释性。

### Q3：当前 embedding 是生产级的吗？

不是。当前是 deterministic hashing embedding，用于本地可运行的 prototype。生产化时可以替换为 OpenAI embeddings、sentence-transformers 或 bge 系列模型。

### Q4：如果 Qdrant 挂了怎么办？

Retriever 会 fallback 到 keyword retriever，Agent 不会整体失败。测试中也覆盖了 Qdrant 不可用时 fallback 生效。

### Q5：这个项目和普通客服机器人区别是什么？

普通客服机器人更偏对话；这个项目偏业务流程和结构化决策支持，输出 AgentResult、候选产品、缺失信息、Retrieved Knowledge、Agent Trace 和 ReviewLog。

### Q6：为什么不自动报价？

工业品报价涉及型号确认、数量、库存、交期、运输、付款条款和认证等因素，自动报价风险很高。当前系统定位为 quotation preparation 前的需求确认辅助。

## 10. 不要夸大的边界说明

面试或 GitHub 展示中应明确说明：

- 当前使用高仿真模拟数据，不是真实企业客户数据。
- 当前不是完整生产系统，是工程化 prototype / portfolio project。
- 当前不自动报价。
- 当前不承诺库存。
- 当前不承诺交期。
- 当前不自动发送邮件。
- 当前没有接入 CRM / ERP / 邮件系统 / 登录权限 / Redis。
- 当前 hashing embedding 不是生产级语义 embedding。

## 11. 必备关键词

- FastAPI
- Next.js
- PostgreSQL
- Docker Compose
- Qdrant
- RAG
- Agent Workflow
- Human-in-the-loop
- Keyword Fallback
- Bilingual UI
- Industrial Automation
- Export Sales

## 12. A7 Knowledge Base Admin 求职亮点

A7 在 Qdrant RAG 基础上补齐了轻量知识库运维后台，可作为面试中的工程完整性亮点：

- 新增 `/knowledge` 页面，用于查看 Qdrant collection 状态、points_count、vector_size、embedding provider 和 keyword fallback。
- 新增 `GET /api/knowledge/status`、`GET /api/knowledge/chunks`、`POST /api/knowledge/reindex`。
- 支持查看 chunks 列表、按 `source_file` 筛选，并手动 `Rebuild Qdrant Index`。
- 浏览器复测确认 `/knowledge`、`/analyze` 和 review 流程均可用，console error count = 0。

面试表达建议：

```text
我没有把 RAG 做成后端黑盒，而是补了一个轻量 Knowledge Base Admin。
它可以查看 Qdrant 是否可用、collection 中有多少 points、当前 embedding 方案是什么，
也可以手动 rebuild index。这个页面不做上传、编辑或删除，主要用于 prototype 的可观测性和运维展示。
```

边界说明：A7 不是完整知识库管理系统，暂不支持知识文件上传、在线编辑、删除、权限控制或异步任务队列。
