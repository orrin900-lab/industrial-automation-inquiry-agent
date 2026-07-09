# A-Final 客服/业务员后台最终集成版验收计划

## 1. A-Final 功能清单

- Public Website Inquiry：`/public-inquiry` 未登录官网询盘模拟入口。
- Email Inquiry Import：`/analyze` 支持 Email Inquiry 模式，标准化为 `InquiryInput`。
- Customer / Sales Console：登录后访问 Dashboard、Analyze、Inquiry List、Inquiry Detail。
- Inquiry List：支持 `channel`、`status`、`product_category` 筛选。
- Inquiry Detail：展示原始询盘、AgentResult、需求确认卡、候选产品、RAG 来源、Agent Trace、Review Logs。
- Requirement Confirmation Card：汇总产品类别、抽取参数、缺失信息、追问问题、风险提示与置信度。
- Reply Draft Workspace：支持编辑、Copy Reply、Export Markdown。
- Human Review：继续记录 reviewer、role、review status、edited reply、reviewer note、review time。
- Follow-up Status：支持 `new`、`analyzed`、`need_clarification`、`draft_ready`、`reviewed`、`followed_up`、`closed`、`lost`。
- Product Library Admin：`/products` 仅 admin 可访问，支持列表、筛选、搜索、新增和启用/停用。
- Knowledge Upload：`/knowledge` 支持上传 `.md` 文件到安全目录，并手动 Rebuild Qdrant Index。
- Redis 基础接入：Docker Compose 增加 Redis，`/api/system/status` 显示 `redis_available`。

## 2. 验收标准

| Area | Acceptance |
| --- | --- |
| Auth | admin / sales / support 可登录；后台页面需要登录；admin-only 页面有权限限制 |
| Inquiry | Public inquiry 可创建记录；Website / Email Analyze 可返回 AgentResult |
| Agent | 意图识别、产品类别、参数抽取、缺失信息、候选产品、英文回复草稿、风险提示保持可用 |
| RAG | Qdrant retrieval 和 keyword fallback 不破坏，Retrieved Knowledge 结构保持兼容 |
| Review | 人工审核可提交，edited reply 可保存，reviewer role 可记录 |
| Product Admin | admin 可查看、搜索、新增、启用/停用 demo 产品 |
| Knowledge Admin | admin 可上传 `.md`，并手动 rebuild index |
| Redis | Redis 不可用时系统不崩溃 |
| Docker | postgres / backend / frontend / qdrant / redis 一键启动 |

## 3. 角色权限

- `admin`：可访问 Knowledge Base Admin、Product Library Admin、Inquiry Console。
- `sales`：可访问询盘分析、询盘列表、询盘详情和 Review，不可访问 Knowledge/Product Admin。
- `support`：可访问询盘处理和 Review，不可访问 Knowledge/Product Admin。
- 未登录用户：仅可访问 `/public-inquiry` 和 `/login`。

## 4. 业务边界

- No automatic quotation。
- No stock commitment。
- No delivery commitment。
- No automatic email sending。
- English reply draft must be reviewed by a human sales/support user。
- 当前产品数据仍为高仿真模拟数据。
- 当前项目是 portfolio / prototype 工程化项目，不是完整生产系统。

## 5. 不做事项

- 不接真实 ERP / CRM。
- 不接 Gmail / Outlook API。
- 不做真实库存同步。
- 不做报价系统。
- 不做自动发邮件。
- 不做复杂在线知识库编辑。
- 不做 Redis 队列、Celery 或分布式锁。

## 6. Docker Compose 启动说明

```powershell
cd "D:\Codex项目文件夹\外贸客服Agent\industrial-inquiry-agent"
docker-compose up -d --build
```

访问地址：

- Frontend: `http://127.0.0.1:3001`
- Backend API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Qdrant: `http://127.0.0.1:6333`
- Redis: `127.0.0.1:6379`

## 7. 最终测试清单

- `/login`
- `/public-inquiry`
- `/analyze` Website Inquiry
- `/analyze` Email Inquiry
- `/inquiries`
- `/inquiries/{id}`
- `/products`
- `/knowledge`
- `/api/system/status`
- `python -m pytest`
- `npm run build`
- `docker-compose config`
- `docker-compose up -d --build`

## 8. A-Final.5 验收记录

- Docker Compose：PASS，`postgres` / `backend` / `frontend` / `qdrant` / `redis` 可启动，backend/frontend/redis healthy。
- Backend pytest：PASS，39 passed。
- Frontend build：PASS，Next.js build passed。
- HTTP/API 回归：PASS，`/login`、`/public-inquiry`、`/analyze`、`/inquiries`、`/knowledge`、`/products`、`/api/system/status` 均验证可用。
- Role Access：PASS，admin 可访问 Knowledge/Product Admin，sales 访问返回 403。
- Knowledge Upload：PASS，非 `.md` 被拒绝，`.md` 上传成功。
- Business Boundary：PASS，系统仍不自动报价、不承诺库存、不承诺交期、不自动发送邮件。

截图状态：A-Final 页面截图 16-20 暂为 pending，需要用户手动截取真实页面；不得引用不存在的图片。
