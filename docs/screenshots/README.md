# 截图清单 Screenshots

本目录保存项目真实运行截图。不要添加伪造截图。

| File | Status | 展示内容 |
| --- | --- | --- |
| `01_dashboard.png` | captured | Dashboard 首页、backend health、统计卡片、最近询盘。 |
| `02_analyze_form.png` | captured | Analyze Inquiry 表单、样例加载、message 输入框、提交按钮。 |
| `03_agent_result.png` | captured | AgentResult 结构化结果、参数抽取、追问问题。 |
| `04_inquiry_list.png` | captured | 询盘列表、status/category/confidence 字段和筛选入口。 |
| `05_inquiry_detail.png` | captured | 询盘详情顶部、原始询盘和 AgentResult 区域。 |
| `06_candidate_products.png` | captured | Candidate Products 候选产品、match_score、match_reason。 |
| `07_retrieved_knowledge.png` | captured | Retrieved Knowledge 检索来源、source_file、section_title、score。 |
| `08_agent_trace.png` | captured | Agent Trace 执行轨迹、mode、success、latency、output_summary。 |
| `09_review_form.png` | captured | English Reply Draft、Human Review 表单和 Review Logs。 |
| `10_swagger_api.png` | captured | FastAPI Swagger API。 |
| `11_docker_compose_running.png` | pending | Docker Desktop 或终端 `docker-compose ps` 的 healthy 状态。 |

## 建议补充截图

`11_docker_compose_running.png` 仍可手动补充，内容建议包含：

```text
industrial-agent-postgres healthy
industrial-agent-backend healthy
industrial-agent-frontend healthy
```

## 截图流程

1. 启动 `docker-compose up -d`。
2. 打开 `http://127.0.0.1:3001`。
3. 截取 Dashboard。
4. 进入 Analyze 页面，加载 PLC 或 VFD sample。
5. 提交分析并截取 AgentResult。
6. 进入详情页，截取 Candidate Products、Retrieved Knowledge、Agent Trace、Review Form。
7. 打开 `http://127.0.0.1:8000/docs` 截取 Swagger。
