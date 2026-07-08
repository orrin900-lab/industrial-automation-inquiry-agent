# 面试讲解 Interview Guide

## 1. 30 秒项目介绍

Industrial Automation Inquiry Agent 是一个面向工业自动化外贸询盘的 full-stack AI Agent 项目。它帮助客服和外贸业务员处理 PLC、VFD、HMI、工业交换机等产品询盘，把英文原始询盘转成结构化 `AgentResult`，并展示候选产品、缺失信息、Qdrant RAG 检索来源、Agent Trace、风险提示和英文回复草稿。系统使用 Next.js、FastAPI、PostgreSQL、Qdrant 和 Docker Compose，并保留 Human-in-the-loop 人工审核。

## 2. 2 分钟项目介绍

这个项目从 C+ Streamlit 原型演进到 A 阶段工程化版本。C+ 阶段先验证 Agent workflow、fallback 规则、可选 LLM JSON 抽取、轻量 RAG、Agent Trace 和结构化输出。A 阶段逐步加入 FastAPI API、PostgreSQL 持久化、Next.js 前端后台、Docker Compose 一键启动、中英文 UI 切换，以及 A6 的 Qdrant-based Vector Retrieval + Keyword Fallback。

项目不是自动客服或自动报价系统，而是帮助业务员做询盘资格确认和风险控制。它不会自动报价、不会承诺库存、不会承诺交期，也不会自动发送邮件；英文回复只是 draft，必须由业务员人工审核。

## 3. 技术架构讲解

- Frontend: Next.js + TypeScript + Tailwind CSS。
- Backend: FastAPI + Pydantic + SQLAlchemy。
- Database: PostgreSQL，开发时保留 SQLite fallback。
- Vector DB: Qdrant。
- Agent Core: intent classifier、category classifier、requirement extractor、retriever、product matcher、reply draft generator、risk checker。
- RAG: Markdown loader + heading splitter + deterministic hashing embedding + Qdrant retrieval + keyword fallback。
- Deployment: Docker Compose 启动 postgres、qdrant、backend、frontend。

## 4. Agent 工作流讲解

Agent 接收 `InquiryInput` 后依次执行：

1. Intent Classifier：识别客户意图。
2. Product Category Classifier：判断 PLC / VFD / HMI / Industrial Switch。
3. Requirement Extractor：抽取 brand、model、quantity、technical_specs 等字段。
4. Missing Info Checker：判断缺失信息。
5. Knowledge Retriever：优先 Qdrant 检索知识库，不可用时 keyword fallback。
6. Product Matcher：从 `products.csv` 推荐候选产品。
7. Reply Draft Generator：生成英文回复草稿。
8. Risk Checker：检查报价、库存、交期、兼容性等风险。
9. Final AgentResult：返回结构化 JSON。

每一步都会写入 Agent Trace，方便解释和排查。

## 5. 为什么要从 keyword RAG 升级到 Qdrant RAG？

keyword RAG 对原型很轻，适合快速验证，但只能做关键词匹配，不能很好处理语义相近表达，也不适合未来更大的知识库。Qdrant 可以把知识 chunk 写成向量索引，让系统结构更接近真实 RAG 工程，也为后续升级 OpenAI embeddings、sentence-transformers 或 bge 模型留出接口。

## 6. Qdrant 在项目中的作用是什么？

Qdrant 用来保存 Markdown 知识库 chunks 的向量索引。Agent 在分析询盘时，会把 query 转成 embedding，再从 Qdrant 检索相关 FAQ、选型规则和邮件模板片段，返回到 `retrieved_knowledge`，供回复草稿和前端展示使用。

当前 collection 是：

```text
industrial_agent_knowledge
```

当前索引 chunks 数量是：

```text
21
```

## 7. 为什么保留 keyword fallback？

RAG 是辅助能力，不应该让整个询盘分析因为 Qdrant 故障而失败。保留 keyword fallback 有三个好处：

- Demo 更稳定，Qdrant 不可用时仍能运行。
- 生产工程上更稳健，避免单点依赖。
- 便于测试和排障，Agent Trace 可以显示 `qdrant` 或 `keyword_fallback`。

## 8. 当前 deterministic hashing embedding 的优缺点？

优点：

- 本地运行。
- 无 API Key。
- 无外部模型下载。
- 结果稳定。
- 适合 prototype 和面试演示。

缺点：

- 语义能力有限。
- 不等同于生产级 embedding。
- 对复杂同义表达、多语言和长文本语义理解能力有限。

所以我会明确说它是 prototype lightweight embedding，不会夸大成生产级语义检索。

## 9. 为什么不直接用 OpenAI embedding？

本项目优先保证本地可运行和可演示，不依赖外部 API Key，也避免网络或额度问题影响作品集展示。当前先用 hashing embedding 保持架构完整，后续可以在同一个 `EmbeddingProvider` 接口下替换为 OpenAI embeddings、sentence-transformers 或 bge 模型。

## 10. Agent Trace 如何体现可观测性？

Agent Trace 记录每个节点：

- `step_name`
- `mode`
- `input_summary`
- `output_summary`
- `success`
- `error_message`
- `latency_ms`

A6 后，Knowledge Retriever 节点可以显示：

- `qdrant`
- `keyword_fallback`
- `retrieval`

这样可以一眼看出本次分析是否真正使用了 Qdrant，或者是否发生了 fallback。

## 11. 项目的业务边界是什么？

边界非常明确：

- 不自动报价。
- 不承诺库存。
- 不承诺交期。
- 不自动发送邮件。
- 英文回复草稿必须人工审核。
- 当前产品数据是高仿真模拟数据。
- 当前不是完整 CRM / ERP / 邮件系统。

这也是项目设计 Human-in-the-loop 的原因。

## 12. 如果面试官问“这是不是生产级 RAG”，怎么回答？

可以这样答：

“目前它是工程化 prototype，不是完整生产级 RAG。A6 已经把 lightweight keyword retriever 升级成 Qdrant-based vector retrieval，并保留 keyword fallback，接口和可观测性都比较接近生产架构。但 embedding 仍是 deterministic hashing embedding，主要为了本地可运行和演示稳定。生产化时我会替换为 OpenAI embeddings、sentence-transformers 或 bge 系列模型，并增加知识库管理、索引任务、评估集、权限和监控。”

## 13. 后续如何升级成生产级知识库？

后续路线：

1. 增加 Knowledge Base Admin，用于上传、查看和管理知识文档。
2. 增加索引构建任务和索引状态展示。
3. 替换为生产级 embedding 模型。
4. 增加 chunk 版本管理和增量更新。
5. 增加检索评估集，评估 recall、precision 和业务命中率。
6. 增加权限、审计日志和监控指标。

## 14. 这和普通客服机器人有什么区别？

普通客服机器人偏自然语言对话；这个项目偏业务流程和结构化决策支持。它输出的是 `AgentResult`，包含参数抽取、缺失信息、候选产品、RAG 来源、Agent Trace、风险提示和人工审核状态，适合沉淀到业务系统中，而不是只生成一段聊天回复。

## 15. LLM 出错怎么办？

系统默认支持 fallback：

- 没有 API Key 时使用规则逻辑。
- LLM 返回非法 JSON 时 fallback 到规则抽取。
- Qdrant 不可用时 fallback 到 keyword retriever。
- Agent Trace 会记录节点 mode 和错误摘要。
- Risk Checker 会持续阻止报价、库存、交期等不安全承诺。

## 16. 如何讲这个项目的技术亮点？

可以按这条线讲：

1. 真实业务场景：工业自动化外贸询盘参数复杂、信息不完整、回复风险高。
2. Agent workflow：不是简单聊天，而是结构化分析链路。
3. 工程闭环：FastAPI、Next.js、PostgreSQL、Qdrant、Docker Compose。
4. 可观测性：Agent Trace 和 Retrieved Knowledge。
5. 可降级：LLM fallback 和 Qdrant keyword fallback。
6. 风险控制：Human-in-the-loop，不自动报价、不自动发邮件。
7. 可演进：embedding、知识库后台、权限、CRM/ERP、邮件系统都能继续扩展。

## A7 面试讲解：Knowledge Base Admin

**为什么要做 Knowledge Base Admin？**

A6 已经把轻量 keyword RAG 升级为 Qdrant-based Vector Retrieval + Keyword Fallback，但面试或演示时还需要让评审看到知识库不是黑盒。因此 A7 增加了轻量运维后台，用来查看 collection 状态、points_count、chunks 列表和手动 rebuild index。

**A7 做了什么？**

- 前端新增 `/knowledge` 页面。
- 后端新增 `GET /api/knowledge/status`、`GET /api/knowledge/chunks`、`POST /api/knowledge/reindex`。
- 支持查看 Qdrant availability、RAG mode、embedding provider、keyword fallback 和 source files。
- 支持从 Qdrant scroll payload 查看 chunks。
- 支持同步 rebuild Qdrant index。

**A7 没做什么？**

当前不是完整知识库管理系统，不支持上传、在线编辑、删除 chunk、登录权限、Redis 异步任务、邮件系统、CRM/ERP 或报价系统。这样控制范围可以保持项目作为 portfolio / prototype 的清晰边界。

**面试时怎么讲亮点？**

可以强调：这个项目不是只把 RAG 写在后端，而是补了运维可观测性。业务员或开发者可以在 UI 中看到 Qdrant 是否可用、当前 collection 中有多少 points、哪些 Markdown source 已被索引，并可以手动 rebuild。Qdrant 不可用时，Agent 仍能 keyword fallback，避免分析链路整体失败。
