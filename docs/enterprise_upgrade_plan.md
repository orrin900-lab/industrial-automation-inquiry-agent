# A+ 企业级增强版路线图 Enterprise Upgrade Plan

## 1. 当前项目状态

Industrial Automation Inquiry Agent 当前已经完成稳定作品集版本：

- FastAPI backend：封装询盘分析、人工审核、知识库运维 API。
- Next.js frontend：客服/外贸业务员后台，支持中英文 Bilingual UI。
- PostgreSQL persistence：保存 inquiry、AgentResult、Agent Trace、Review Logs。
- Qdrant RAG：基于 Markdown 知识库构建向量检索，并保留 Keyword Fallback。
- Docker Compose：一键启动 PostgreSQL、Qdrant、backend、frontend。
- Human-in-the-loop：英文回复草稿必须由业务员人工审核。
- Knowledge Base Admin：查看 Qdrant 状态、chunks、手动 rebuild index。

当前版本定位是 portfolio / prototype 工程化项目，不是完整生产系统。产品数据为高仿真模拟数据。

## 2. 为什么需要 A+ 企业级增强版

A1-A7 已经证明了端到端业务闭环，但如果进一步接近企业内部系统，需要补强：

- 身份认证与角色权限，避免后台功能完全公开。
- 数据适配层，方便后续从 CSV 切换到数据库、ERP、CRM 或邮件系统。
- 邮件询盘导入增强，让业务入口更贴近外贸场景。
- 评估与监控能力，用于持续观察 Agent、RAG、人工审核质量。

A+ 阶段的重点不是扩大功能表面，而是增强“可治理、可维护、可演示生产化路径”的工程能力。

## 3. A+ 总体目标

将当前稳定 prototype 升级为更接近企业后台的 AI Agent 应用骨架：

- A8：Auth & Role-Based Access，增加 demo 用户、角色和基础权限控制。
- A9：Business Data Adapter Layer，规划真实业务数据接入抽象。
- A10：Email Inquiry Import Enhancement，规划邮件询盘导入增强。
- A11：Evaluation & Monitoring Enhancement，规划评估与监控看板。

## 4. A8-A11 阶段规划

| 阶段 | 名称 | 目标 | 本阶段是否写代码 |
| --- | --- | --- | --- |
| A8 | 权限与角色 Auth & Roles | 登录、当前用户、admin/sales/support、Knowledge Base Admin 权限限制 | 是 |
| A9 | 业务数据适配 Business Data Adapters | 规划 ProductDataProvider / InquirySourceProvider 抽象 | 否，本轮只做设计 |
| A10 | 邮件询盘导入 Email Import | 规划邮件标题、发件人、正文、联系方式识别和回复草稿流程 | 否，本轮只做设计 |
| A11 | 评估与监控 Evaluation & Monitoring | 规划 RAG 命中、风险、置信度、人工审核状态统计 | 否，本轮只做设计 |

## 5. 每阶段开发边界

### A8 边界

做：

- Demo 用户登录 / 登出。
- 当前用户信息 API。
- admin / sales / support 三类角色。
- `/api/knowledge/*` 限制为 admin。
- 前端根据角色显示或限制 Knowledge Base Admin。
- Review 操作尽量记录当前登录用户。

不做：

- SSO、OAuth、多租户、复杂组织架构。
- 密码找回、手机验证码、字段级权限。
- 真实企业账号系统。

### A9 边界

只做规划，不写代码：

- ProductDataProvider 抽象。
- CSVProductProvider 保留。
- DatabaseProductProvider / ERPProductProvider 预留。
- InquirySourceProvider 抽象。
- WebsiteInquiryProvider / EmailInquiryProvider 预留。

### A10 边界

只做规划，不写代码：

- 邮件标题、发件人、正文解析。
- 客户公司、国家、联系方式识别。
- 英文回复草稿展示、复制、Markdown 导出。

不自动发送邮件。

### A11 边界

只做规划，不写代码：

- Agent 分析质量记录。
- RAG mode 和 Qdrant 命中来源统计。
- confidence_score 分布。
- risk_flags 和 manual review status 统计。
- 失败案例列表与 Evaluation Dashboard 规划。

## 6. 每阶段验收标准

| 阶段 | 验收标准 |
| --- | --- |
| A8 | backend pytest 通过；frontend build 通过；Docker Compose 正常；admin 可访问 `/knowledge`；非 admin 被限制；`/analyze` 和 review 不回归 |
| A9 | 文档说明数据适配抽象、边界、后续任务和 Codex 提示词 |
| A10 | 文档说明邮件导入增强流程、字段、边界和后续任务 |
| A11 | 文档说明评估指标、看板结构、监控边界和后续任务 |

## 7. 分支与 tag 策略

- 稳定主线：`main`
- A8 开发分支：`feature/a8-auth-roles`
- A8 功能 tag：`a8-auth-roles`
- A8 稳定 tag：`a8-auth-roles-stable`
- A+ 路线图 tag：`a-plus-roadmap-ready`

禁止使用 `git push --force`。如遇 merge conflict、测试失败、网络认证失败，应停止并记录。

## 8. 风险控制

- 保留 Keyword Fallback，避免 Qdrant 不可用导致 Agent 失败。
- 保留无 LLM API Key fallback，Demo 必须可运行。
- Auth 阶段使用 demo 用户时必须明确 prototype 边界。
- 不写入真实 API Key、secret、token、password。
- 不删除用户文件、不修改 C+ 项目。
- 不自动报价、不承诺库存、不承诺交期、不自动发送邮件。

## 9. 不做事项清单

A+ 当前不做：

- 真实企业 SSO / OAuth。
- 多租户 / 复杂组织架构。
- Redis。
- CRM / ERP 正式集成。
- 邮件自动发送。
- 报价系统。
- 库存和交期承诺。
- 知识库上传、在线编辑、删除。
- 生产级向量模型效果承诺。

## 10. 最终交付形态

A+ 完成后，项目应具备：

- 可登录的业务后台骨架。
- 基础角色权限。
- 更清晰的数据适配路线。
- 更贴近外贸邮件场景的后续导入方案。
- 可用于面试讲解的评估与监控增强规划。
- 继续保持 portfolio / prototype 工程化项目定位。

