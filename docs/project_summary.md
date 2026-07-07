# 项目总结 Project Summary

## 1. 项目定位

Industrial Automation Inquiry Agent 是一个面向工业自动化外贸业务的 full-stack AI Agent 原型。项目重点不是自动成交，而是帮助客服 / 外贸业务员完成技术询盘的需求确认、风险识别和人工审核。

## 2. 已完成能力

- FastAPI backend 封装 Agent Core。
- Next.js + TypeScript + Tailwind CSS 前端后台。
- PostgreSQL 持久化 inquiry、AgentResult、AgentRun、AgentStep、ReviewLog。
- SQLite fallback 便于本地开发。
- Docker Compose 一键启动 frontend、backend、postgres。
- 规则 fallback + 可选 LLM JSON 抽取。
- 轻量 RAG：Markdown loader、splitter、keyword retriever。
- Product Repository 和 Candidate Products 匹配。
- Agent Trace 可观测性。
- Retrieved Knowledge 来源展示。
- Human Review 人工审核表单和 Review Logs。
- 中英文 UI 切换，默认中文，并使用 `localStorage` 保持选择。
- README、docs、截图和人工复测报告已整理为作品集展示材料。

## 3. 当前技术栈

- Frontend: Next.js, TypeScript, Tailwind CSS, App Router
- Backend: FastAPI, Pydantic, SQLAlchemy
- Database: PostgreSQL, SQLite fallback
- Agent Core: rule fallback, optional LLM extraction
- RAG: lightweight keyword retrieval
- DevOps: Docker Compose
- Testing: pytest, Next.js build

## 4. 当前业务闭环

1. 业务员提交官网或邮件询盘。
2. 后端保存 inquiry。
3. Agent Core 执行分析。
4. 后端保存 AgentResult、AgentRun、AgentStep。
5. 前端展示结构化分析结果。
6. 业务员编辑 English Reply Draft。
7. 业务员提交 Human Review。
8. Review Log 持久化。

## 5. 工程化程度

项目已经从 C+ 原型演进到 A 阶段工程化版本：

- API 层与 Agent 业务逻辑分离。
- Repository / Retriever 接口边界清晰。
- Docker Compose 已实际验收通过。
- P0/P1 人工复测通过。
- 前端以结构化区块展示 AgentResult，而不是只展示 JSON。
- Agent Trace 和 Retrieved Knowledge 提升可解释性。

## 6. 当前限制

- 产品和询盘数据为高仿真模拟数据。
- 轻量 RAG 不是生产级向量数据库。
- 未接入 Qdrant、Redis、CRM、ERP、邮件系统。
- 未接入登录权限。
- 不自动报价、不承诺库存、不承诺交期、不自动发送邮件。
- 当前评估不代表真实生产准确率。

## 7. 后续路线

推荐下一步进入 A6：Qdrant RAG Enhancement。

建议范围：

1. docker-compose 增加 Qdrant。
2. backend 增加 Qdrant 配置。
3. Markdown 知识库切 chunk 后写入 Qdrant。
4. 增加 embedding 层。
5. Retriever 支持 Qdrant 检索。
6. 保留 keyword fallback。
7. 不破坏 `AgentResult.retrieved_knowledge` 结构。
8. 前端 Retrieved Knowledge 展示保持兼容。
9. 增加测试。
10. 更新 README 和 docs。
