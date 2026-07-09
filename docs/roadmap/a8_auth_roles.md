# A8 权限与角色系统 Auth & Role-Based Access

## 1. 阶段目标

A8 目标是在当前后台基础上增加轻量权限与角色系统，让项目从公开 Demo 更接近业务后台形态。

核心能力：

- 登录 / 登出。
- 当前用户信息。
- demo 用户体系。
- admin / sales / support 三类角色。
- API 基础鉴权。
- 前端根据角色显示导航入口。
- Knowledge Base Admin 限制为 admin。
- Review 记录当前用户。

## 2. 建议 demo 用户

| Email | Password | Role | 用途 |
| --- | --- | --- | --- |
| `admin@example.com` | `admin123` | `admin` | 系统管理员，可访问 Knowledge Base Admin |
| `sales@example.com` | `sales123` | `sales` | 外贸业务员，可分析询盘和提交 Review |
| `support@example.com` | `support123` | `support` | 客服支持，可查看和处理询盘 |

这些账号仅用于作品集 demo，不代表真实生产账号系统。

## 3. 后端范围

建议新增：

- `backend/app/api/auth.py`
- `backend/app/schemas/auth.py`
- `backend/app/services/auth_service.py`
- `backend/app/core/security.py`
- `backend/app/core/dependencies.py`
- `backend/tests/test_auth_api.py`
- `backend/tests/test_role_access.py`

建议 API：

```text
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/logout
```

权限要求：

- `/api/knowledge/status`
- `/api/knowledge/chunks`
- `/api/knowledge/reindex`

以上知识库 API 仅允许 `admin` 访问。

## 4. 前端范围

建议新增：

- `frontend/app/login/page.tsx`
- `frontend/lib/auth.ts`
- `frontend/components/AuthGuard.tsx`
- `frontend/components/UserMenu.tsx`

前端行为：

- `/login` 提供 demo 登录。
- 登录后保存 token。
- 顶部显示当前用户和角色。
- 支持退出登录。
- admin 显示 Knowledge Base 入口。
- 非 admin 访问 `/knowledge` 时显示无权限。
- `/analyze`、`/inquiries`、Review 流程保持可用。
- 中文 / English 文案保持可切换。

## 5. 暂不做

- SSO。
- OAuth。
- 多租户。
- 复杂组织架构。
- 密码找回。
- 手机验证码。
- 字段级权限。
- 真实生产账号管理后台。

## 6. 验收标准

- admin / sales / support 可以登录。
- `GET /api/auth/me` 返回当前用户。
- admin 可以访问 `/knowledge`。
- sales / support 不能访问 `/knowledge` 或看到无权限提示。
- Review 提交时能记录当前用户。
- backend pytest 通过。
- frontend build 通过。
- Docker Compose 正常。
- `/analyze` 仍可用。
- review 仍可提交。

