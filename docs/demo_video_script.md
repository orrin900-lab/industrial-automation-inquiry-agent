# 录屏演示脚本 Demo Video Script

## 1. 3 分钟版

目标：快速展示项目定位、完整链路和技术亮点。

时间安排：

| 时间 | 内容 |
| --- | --- |
| 0:00-0:20 | 打开 README，说明项目是工业自动化外贸询盘 AI Agent。 |
| 0:20-0:40 | 展示 Docker Compose 服务：PostgreSQL、Qdrant、FastAPI backend、Next.js frontend。 |
| 0:40-1:10 | 打开 Dashboard，展示 backend health、统计卡片、最近询盘。 |
| 1:10-1:40 | 进入 Analyze 页面，加载 PLC sample 并提交分析。 |
| 1:40-2:20 | 展示 AgentResult、Candidate Products、Missing Information、English Reply Draft。 |
| 2:20-2:45 | 展示 Retrieved Knowledge 和 Agent Trace，强调 `Knowledge Retriever=qdrant`。 |
| 2:45-3:00 | 展示 Human Review，说明不自动报价、不自动发送邮件，最后总结技术栈。 |

## 2. 5 分钟版

目标：更适合面试或作品集讲解，补充架构与测试材料。

时间安排：

| 时间 | 内容 |
| --- | --- |
| 0:00-0:30 | README 首屏：项目定位、技术栈、业务边界。 |
| 0:30-0:55 | Docker Compose 状态：postgres、qdrant、backend、frontend。 |
| 0:55-1:25 | Dashboard：首页、backend health、最近询盘。 |
| 1:25-1:45 | 展示中文 / English 切换。 |
| 1:45-2:25 | Analyze 页面：加载 PLC 或 VFD sample，提交英文询盘。 |
| 2:25-3:05 | AgentResult：参数抽取、缺失信息、候选产品、风险提示。 |
| 3:05-3:35 | Retrieved Knowledge：source_file、section_title、score、content preview。 |
| 3:35-4:00 | Agent Trace：解释 `qdrant`、`fallback`、`rule` mode。 |
| 4:00-4:25 | Inquiry Detail + Human Review：编辑草稿、提交 review。 |
| 4:25-4:45 | 打开 `docs/manual_test_report.md` 和 `docs/qdrant_rag_summary.md`。 |
| 4:45-5:00 | 总结：FastAPI、Next.js、PostgreSQL、Qdrant RAG、Keyword Fallback、Human-in-the-loop。 |

## 3. 录屏操作步骤

1. 打开项目根目录 README。
2. 打开终端，执行或展示：

```powershell
docker-compose ps
```

3. 如需展示 Qdrant index build：

```powershell
docker-compose exec backend python scripts/build_qdrant_index.py
```

4. 打开前端：

```text
http://127.0.0.1:3001
```

5. Dashboard 展示 backend health 和最近询盘。
6. 点击语言切换，展示中文 / English。
7. 进入 `/analyze`。
8. 选择 PLC 或 VFD sample。
9. 点击 Analyze。
10. 展示返回的 `inquiry_id`、`agent_result_id` 和 AgentResult。
11. 展示 Candidate Products。
12. 展示 Retrieved Knowledge。
13. 展示 Agent Trace，重点指出 `Knowledge Retriever=qdrant`。
14. 点击进入 Inquiry Detail。
15. 编辑 English Reply Draft 或 reviewer note。
16. 提交 Human Review。
17. 打开 `docs/manual_test_report.md`。
18. 打开 `docs/qdrant_rag_summary.md`。

## 4. 旁白稿

“这个项目叫 Industrial Automation Inquiry Agent，是一个面向工业自动化外贸询盘的 AI Agent 原型。它不是自动报价或自动发邮件系统，而是帮助业务员做询盘需求确认、产品候选推荐、风险提示和人工审核。”

“技术上，项目使用 Next.js 做前端后台，FastAPI 做后端 API，PostgreSQL 做业务数据持久化，Qdrant 做 RAG 向量检索，Docker Compose 做本地一键启动。”

“这里我加载一条 PLC 英文询盘。提交后，Agent 会识别客户意图和产品类别，抽取技术参数，比如 16DI、8DO、24V DC、RS485，并判断缺失字段。”

“候选产品来自 products.csv，不是模型凭空生成。Retrieved Knowledge 来自 Markdown 知识库切分后的 chunks，A6 之后已经写入 Qdrant。Agent Trace 这里可以看到 Knowledge Retriever 的 mode 是 qdrant。”

“如果没有 LLM API Key，系统会用规则 fallback；如果 Qdrant 不可用，会自动 fallback 到 keyword retriever，保证 demo 和基础链路不会整体失败。”

“最后，英文回复只是 draft，需要业务员人工审核。系统明确不自动报价、不承诺库存、不承诺交期、不自动发送邮件。”

## 5. 展示重点

- 完整工程链路：Next.js + FastAPI + PostgreSQL + Qdrant + Docker Compose。
- Agent Workflow：结构化分析而不是普通聊天机器人。
- Qdrant RAG：`Retrieved Knowledge` 和 `Knowledge Retriever=qdrant`。
- Keyword Fallback：Qdrant 不可用时仍可运行。
- Agent Trace：可观测、可解释、方便调试。
- Human-in-the-loop：业务员人工审核，风险边界清晰。
- Bilingual UI：中文 / English 切换，适合中文面试展示和英文业务场景。

## 6. 避免夸大的说法

不要说：

- “已经接入真实企业数据。”
- “可以自动报价。”
- “可以自动承诺库存或交期。”
- “可以自动发送邮件给客户。”
- “当前 embedding 是生产级语义模型。”
- “当前系统已经是完整 CRM / ERP。”

推荐说法：

- “这是一个工程化 prototype / portfolio project。”
- “当前使用高仿真模拟数据。”
- “当前 hashing embedding 是 lightweight prototype embedding。”
- “生产化时可以替换为 OpenAI embeddings、sentence-transformers 或 bge 系列模型。”
- “系统定位是 inquiry qualification 和 sales support，不是自动成交系统。”
