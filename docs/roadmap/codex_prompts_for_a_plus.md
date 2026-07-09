# Codex Prompts For A+ Stages

## A8 Prompt

```text
请开始 A8：权限与角色系统 Auth & Role-Based Access。
请基于现有 FastAPI + Next.js 项目新增 demo 登录、当前用户、admin/sales/support 角色、Knowledge Base Admin 权限限制，并保持 /analyze 和 review 流程不回归。
不要接 OAuth、SSO、多租户、短信验证码或真实生产账号系统。
完成后运行 backend pytest、frontend build、docker-compose config/up/ps，并提交 tag a8-auth-roles。
```

## A8.5 Prompt

```text
请执行 A8.5：Auth & Roles 稳定收口。
请复测 /login、admin/sales/support 登录、/knowledge admin 权限、非 admin 无权限、/analyze 和 review 回归。
补充截图、manual_test_report、README/docs，合并回 main，创建 tag a8-auth-roles-stable。
```

## A9 Prompt

```text
请开始 A9：真实业务数据接口预留 Business Data Adapter Layer。
请只实现 provider 抽象和最小兼容，不接真实 ERP/CRM，不导入真实数据，保留 CSV fallback。
```

## A10 Prompt

```text
请开始 A10：邮件询盘导入增强 Email Inquiry Import Enhancement。
请增强邮件输入字段和解析，不自动发送邮件，不接真实邮箱账号，不承诺报价、库存或交期。
```

## A11 Prompt

```text
请开始 A11：评估与监控增强 Evaluation & Monitoring Enhancement。
请基于 PostgreSQL 中已有 inquiry、agent_result、agent_run、agent_step、review_log 数据，新增轻量 Evaluation Dashboard 和 API。
不要接 Prometheus/Grafana，不夸大生产准确率。
```

