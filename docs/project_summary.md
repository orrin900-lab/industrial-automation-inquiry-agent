# 项目总结 Project Summary

## 1. 项目定位

Industrial Automation Inquiry Agent 是一个面向工业自动化外贸业务的 full-stack AI Agent 原型。项目重点不是自动成交，而是帮助客服 / 外贸业务员完成技术询盘的需求确认、风险识别和人工审核。

## 2. 已完成能力

- FastAPI backend 封装 Agent Core。
- Next.js + TypeScript + Tailwind CSS 前端后台。
- PostgreSQL 持久化 inquiry、AgentResult、AgentRun、AgentStep、ReviewLog。
- SQLite fallback 便于本地开发。
- Docker Compose 一键启动 frontend、backend、postgres、qdrant。
- 规则 fallback + 可选 LLM JSON 抽取。
- Qdrant-based Vector Retrieval + Keyword Fallback。
- 本地 deterministic hashing embedding，无 API Key 和模型下载依赖。
- Product Repository 和 Candidate Products 匹配。
- Agent Trace 可观测性。
- Retrieved Knowledge 来源展示。
- Human Review 人工审核表单和 Review Logs。
- 中文 / English UI 切换，默认中文，并使用 `localStorage` 保持选择。
- README、docs、截图和人工复测报告已整理为作品集展示材料。

## 3. 当前技术栈

- Frontend: Next.js, TypeScript, Tailwind CSS, App Router
- Backend: FastAPI, Pydantic, SQLAlchemy
- Database: PostgreSQL, SQLite fallback
- Vector DB: Qdrant
- RAG: Markdown loader, splitter, hashing embedding, Qdrant retrieval, keyword fallback
- Agent Core: rule fallback, optional LLM extraction
- DevOps: Docker Compose
- Testing: pytest, Next.js build

## 4. 当前业务闭环

1. 业务员提交官网或邮件询盘。
2. 后端保存 inquiry。
3. Agent Core 执行分析。
4. Retriever 优先从 Qdrant 检索知识来源，失败时 keyword fallback。
5. 后端保存 AgentResult、AgentRun、AgentStep。
6. 前端展示结构化分析结果。
7. 业务员编辑 English Reply Draft。
8. 业务员提交 Human Review。
9. Review Log 持久化。

## 5. 当前工程化程度

项目已经从 C+ 原型演进到 A 阶段工程化版本：

- API 层与 Agent 业务逻辑分离。
- Repository / Retriever 接口边界清晰。
- Qdrant 检索和 keyword fallback 解耦。
- Docker Compose 已覆盖 PostgreSQL、Qdrant、backend、frontend。
- 前端以结构化区块展示 AgentResult，而不是只展示 JSON。
- Agent Trace 和 Retrieved Knowledge 提升可解释性。

## 6. 当前限制

- 产品和询盘数据为高仿真模拟数据。
- 当前 hashing embedding 是 prototype lightweight embedding，不代表最终生产语义 embedding。
- 未接入登录权限、CRM、ERP、邮件系统、Redis。
- 未提供知识库上传后台。
- 不自动报价、不承诺库存、不承诺交期、不自动发送邮件。
- 当前评估不代表真实生产准确率。

## 7. 后续路线

建议下一轮优先选择：

1. 知识库管理后台：支持查看、上传、重建 Qdrant index。
2. 生产级 embedding：OpenAI embeddings 或 sentence-transformers。
3. 最终简历 / 面试材料整理：将 A6 能力纳入 resume bullets 和 demo script。
4. 登录权限与角色控制。
5. Redis 异步任务和长耗时索引构建。

## 8. A7 知识库运维后台 Knowledge Base Admin

A7 增加了轻量 Knowledge Base Admin，用于作品集原型中的 Qdrant RAG 运维展示：

- 前端新增 `/knowledge` 页面，支持中文 / English 切换。
- 后端新增 `GET /api/knowledge/status`、`GET /api/knowledge/chunks`、`POST /api/knowledge/reindex`。
- 可以查看当前 RAG mode、Qdrant 可用状态、collection、points_count、vector_size、embedding provider 和 keyword fallback 状态。
- 可以查看 Qdrant 中的 knowledge chunks，并按 `source_file` 筛选。
- 可以手动 rebuild Qdrant index，复用现有 Markdown loader、splitter、hashing embedding 和 upsert 逻辑。

当前 A7 仍是轻量运维后台，不支持知识库上传、在线编辑、删除 chunk、登录权限、Redis 异步任务、邮件系统、CRM/ERP 或报价系统。系统仍然不自动报价、不承诺库存、不承诺交期、不自动发送邮件，英文回复草稿必须由业务员人工审核。

## 9. A7.5 稳定收口

A7.5 完成 Knowledge Base Admin 浏览器复测、截图和稳定验证：

- 新增真实截图 `docs/screenshots/12_knowledge_base_admin.png`。
- 新增真实截图 `docs/screenshots/13_knowledge_reindex_success.png`。
- 浏览器验证 `/knowledge` 页面、中文 / English 切换、source_file 筛选、分页、Rebuild Qdrant Index。
- 回归验证 `/analyze`、Retrieved Knowledge、Agent Trace 和 Human Review。
- `points_count` 重建后保持为 `21`，说明 upsert 稳定。

该阶段仍保持 portfolio / prototype 边界，不进入知识库上传、编辑、删除或权限系统。

## 10. 最终求职材料整理 Career Package

方案 A 已完成最终求职材料整理，新增目录 `docs/career_package/`：

- `resume_project_final.md`: 最终简历项目描述，包含中文 / 英文、简短版、标准版、详细版和 bullet points。
- `interview_pitch.md`: 30 秒、1 分钟、3 分钟、5 分钟面试讲解稿。
- `technical_qa.md`: 面试技术追问 Q&A，覆盖 Agent Workflow、RAG、Qdrant、fallback、Human Review、Docker Compose 等问题。
- `project_challenges.md`: 项目难点与解决方案。
- `job_application_notes.md`: 投递岗位、简历写法、面试边界和后续补强建议。

这些材料用于 GitHub 作品集、简历投递、面试讲解和技术追问准备。所有材料继续明确：项目使用高仿真模拟数据，是 portfolio / prototype 工程化项目，不自动报价、不承诺库存、不承诺交期、不自动发送邮件。
