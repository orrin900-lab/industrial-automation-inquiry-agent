# GitHub 发布指南 GitHub Publish Guide

## 1. 推荐仓库名

```text
industrial-automation-inquiry-agent
```

## 2. GitHub Repo Description

```text
An AI-powered inquiry analysis agent for industrial automation export sales, built with FastAPI, Next.js, PostgreSQL, Qdrant RAG, and Docker Compose.
```

## 3. 建议 Topics

- `ai-agent`
- `rag`
- `qdrant`
- `fastapi`
- `nextjs`
- `postgresql`
- `docker-compose`
- `industrial-automation`
- `export-sales`
- `human-in-the-loop`

## 4. 发布前检查

发布前确认：

- 当前分支为 `master`。
- 工作区干净。
- 稳定 tag 存在：`a6-qdrant-rag-stable`。
- `.env`、`.env.local`、数据库文件、`.venv`、`node_modules`、`.next`、Docker volume 数据没有被提交。
- `README.md` 中启动命令、Qdrant index build 命令和业务边界说明完整。
- 截图均为真实运行截图，不引用不存在的图片。

## 5. 首次上传步骤

1. 在 GitHub 创建空仓库。
2. 推荐仓库名使用 `industrial-automation-inquiry-agent`。
3. 不要在 GitHub 初始化 README、`.gitignore` 或 license，避免和本地仓库冲突。
4. 在本地项目根目录设置 remote。

命令模板：

```powershell
cd "D:\Codex项目文件夹\外贸客服Agent\industrial-inquiry-agent"
git remote add origin https://github.com/<your-username>/industrial-automation-inquiry-agent.git
git push -u origin master
```

如果远端已存在：

```powershell
git remote -v
git remote set-url origin https://github.com/<your-username>/industrial-automation-inquiry-agent.git
git push -u origin master
```

## 6. 推送 tags

推送当前稳定 tag：

```powershell
git push origin a6-qdrant-rag-stable
```

推送所有 tags：

```powershell
git push origin --tags
```

## 7. GitHub README 展示建议

建议 README 首屏重点展示：

- 项目定位：Industrial Automation Inquiry Agent。
- 技术栈：FastAPI、Next.js、PostgreSQL、Qdrant、Docker Compose。
- 业务边界：不自动报价、不承诺库存、不承诺交期、不自动发送邮件。
- Quick Start：`docker-compose up --build`。
- Qdrant index build：`docker-compose exec backend python scripts/build_qdrant_index.py`。
- 截图：Dashboard、AgentResult、Retrieved Knowledge、Agent Trace、Swagger。

## 8. 敏感信息注意事项

不要上传：

- `.env`
- `.env.local`
- 真实 API Key
- 数据库文件
- `.venv`
- `node_modules`
- `.next`
- 本地日志
- Docker volume 数据

当前 `.env.example` 只保留占位符和本地 demo 配置，不应写入真实密钥。

## 9. 发布后检查

GitHub 上传后建议检查：

1. README 图片是否正常显示。
2. docs 链接是否能打开。
3. GitHub Topics 是否设置完整。
4. release/tag 是否可见。
5. 仓库没有包含 `.env`、`.env.local`、数据库文件或虚拟环境。
