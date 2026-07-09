# Known Issues 已知事项

## 1. Frontend npm audit

在 Docker frontend 构建过程中，`npm audit` 曾提示：

```text
2 vulnerabilities (1 moderate, 1 critical)
```

当前状态：

- `npm run build` 已通过。
- Docker Compose frontend 构建和运行已通过。
- 本轮 Final Delivery 不升级依赖，避免在最终交付收口阶段引入额外行为变更。

后续建议：

- 单独创建 `dependency-security-cleanup` 分支处理依赖安全升级。
- 执行 `npm audit` 查看具体包和影响范围。
- 优先评估升级是否影响 Next.js 15 / React 19 当前构建链路。
- 升级后重新执行 frontend build、backend pytest、Docker Compose 和核心页面回归。

## 2. Pending A-Final screenshots

以下截图仍为 pending，需要用户在本地真实页面手动截取后补充：

- `docs/screenshots/16_public_inquiry_form.png`
- `docs/screenshots/17_email_inquiry_import.png`
- `docs/screenshots/18_reply_draft_edit_export.png`
- `docs/screenshots/19_product_library_admin.png`
- `docs/screenshots/20_knowledge_upload.png`

当前未伪造截图，也未在 README 中引用不存在的图片。

## 3. Prototype boundaries

当前项目是 portfolio / prototype 工程化项目：

- 使用高仿真模拟数据。
- 未接入真实 ERP / CRM / 邮箱系统。
- 不自动报价。
- 不承诺库存。
- 不承诺交期。
- 不自动发送邮件。
- 英文回复草稿必须人工审核。
