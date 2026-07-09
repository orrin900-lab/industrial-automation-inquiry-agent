# 投递包装说明 Job Application Notes

## 1. 这个项目适合投递哪些岗位

适合：

- AI Agent 应用开发工程师
- 大模型应用开发工程师
- Python 后端开发工程师
- RAG 应用开发工程师
- AI 产品工程师
- 工业 AI 应用方向
- 企业 AI 应用开发方向
- Full-stack AI Application Engineer

尤其适合强调“行业业务理解 + AI 工程落地”的岗位。

## 2. 简历中应该怎么写项目名称

推荐中文：

```text
工业自动化外贸询盘分析与转化辅助 AI Agent
```

推荐英文：

```text
Industrial Automation Inquiry Agent
```

组合写法：

```text
Industrial Automation Inquiry Agent｜工业自动化外贸询盘分析与转化辅助 AI Agent
```

## 3. 简历中不应该怎么写

不要写：

- 已接入真实企业客户数据。
- 已生产上线。
- 能自动报价。
- 能自动发送客户邮件。
- 能准确判断库存和交期。
- 已完成完整 CRM/ERP 集成。
- RAG 已达到生产级语义检索效果。

更稳妥的写法：

```text
基于高仿真模拟数据构建的工程化 AI Agent prototype，用于展示工业自动化外贸询盘需求确认、RAG 检索、人工审核和 Docker Compose 部署能力。
```

## 4. 面试时优先讲哪些亮点

建议优先讲：

1. 工业自动化外贸询盘是有业务复杂度的真实行业场景。
2. Agent Workflow 是结构化流程，不是单次聊天补全。
3. `AgentResult`、`Agent Trace` 和 `Retrieved Knowledge` 提升可解释性。
4. Qdrant RAG + Keyword Fallback 体现工程稳定性。
5. Human-in-the-loop 体现业务风险控制。
6. PostgreSQL 持久化和 Docker Compose 体现工程完整度。
7. Knowledge Base Admin 展示 RAG 运维可观测性。
8. Bilingual UI 适合中文求职展示和英文外贸业务场景。

## 5. 被问没有真实企业数据时怎么回答

可以回答：

```text
这个项目定位是作品集级工程化 prototype，所以我没有使用真实企业数据，也没有上传任何敏感信息。
我用高仿真模拟数据还原工业自动化询盘场景，重点展示业务建模、Agent Workflow、RAG、持久化、前端后台和 Docker Compose 的工程能力。
如果接入真实企业，需要先做数据脱敏、权限、审计和系统集成。
```

## 6. 被问不是生产系统时怎么回答

可以回答：

```text
是的，它不是完整生产系统，我会明确这么说明。
但它已经覆盖生产化前需要验证的关键链路：结构化 AgentResult、fallback、RAG、PostgreSQL、Qdrant、Human Review、Docker Compose 和测试。
后续生产化重点会放在真实数据接入、权限、审计、监控、CI/CD 和生产级 embedding。
```

## 7. 如何把工业自动化经历和 AI Agent 项目连接起来

表达重点：

- 工业自动化产品参数复杂，询盘需要技术理解。
- 外贸业务风险高，不能随便承诺价格、库存和交期。
- AI Agent 适合做需求确认、信息补全、风险提示和回复草稿。
- 你的行业背景帮助你设计更贴近业务的字段、流程和边界。

示例：

```text
我选择这个方向不是随便做一个通用聊天机器人，而是把工业自动化行业里真实存在的询盘确认问题抽象成 AI Agent workflow。
这让我能把原来的行业理解迁移到大模型应用开发里。
```

## 8. 适合投递岗位关键词

- AI Agent
- LLM Application
- RAG
- Qdrant
- FastAPI
- Python Backend
- Next.js
- PostgreSQL
- Docker Compose
- Human-in-the-loop
- Enterprise AI
- Industrial AI
- Workflow Automation
- B2B SaaS
- Export Sales
- Knowledge Base

## 9. 不适合强行投递的岗位

不建议把这个项目作为主打去投：

- 纯算法研究岗。
- 需要大规模模型训练经验的岗位。
- 强 MLOps / Kubernetes / 云原生生产运维岗位。
- 纯前端视觉设计岗位。
- 强实时控制 / PLC 编程岗位。

但它可以作为辅助项目说明你具备 AI 应用工程能力。

## 10. 后续补强方向

如果继续增强求职竞争力，可以按优先级做：

1. 生产级 embedding：OpenAI embeddings、sentence-transformers 或 bge-m3。
2. Knowledge Base Admin 增强：rebuild 日志、collection diagnostics、chunk search。
3. 权限与审计：登录、角色、操作记录。
4. OpenAPI 生成 TypeScript client。
5. CI：GitHub Actions 跑 backend pytest 和 frontend build。
6. 邮件导入：只做 draft/import，不自动发送。
7. CRM/ERP mock integration：继续保持报价和库存人工确认边界。

## 11. A-Final 投递包装建议

当前 A-Final 可以在简历中包装为：

```text
工业自动化外贸询盘客服/业务员后台 AI Agent
```

推荐强调：

- 不是单点 chatbot，而是完整客服 / 业务员工作台。
- 覆盖 Public Inquiry、Email Inquiry Import、Inquiry Console、Human Review、Product Library Admin、Knowledge Upload。
- 具备 FastAPI、Next.js、PostgreSQL、Qdrant、Redis、Docker Compose 的工程化链路。
- 保留 Human-in-the-loop 和业务风险边界。

不要写：

- 已接入真实企业 ERP / CRM。
- 已自动报价。
- 已自动发送客户邮件。
- 已在生产环境上线。

更稳妥的表达是：这是一个 portfolio / prototype 工程化项目，使用高仿真模拟数据验证企业 AI Agent 后台的设计与实现能力。
