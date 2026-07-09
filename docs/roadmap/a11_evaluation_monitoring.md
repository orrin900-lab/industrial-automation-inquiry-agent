# A11 评估与监控增强 Evaluation & Monitoring Enhancement

## 1. 阶段目标

A11 目标是规划 Agent、RAG 和人工审核质量的评估与监控能力，帮助项目从“能跑”走向“可观察、可复盘、可改进”。

本阶段只做路线图和技术设计，不开发代码。

## 2. 计划指标

- Agent 分析质量记录。
- RAG mode 统计：qdrant / keyword_fallback。
- Qdrant 命中来源统计：source_file、section_title。
- confidence_score 分布。
- risk_flags 统计。
- manual review status 统计。
- 失败案例列表。
- 平均处理耗时。
- Agent Trace 节点耗时分布。

## 3. Evaluation Dashboard 规划

建议页面：

```text
/evaluation
```

看板区域：

- 总分析次数。
- 平均置信度。
- Qdrant 使用率。
- Keyword Fallback 触发率。
- 风险提示 Top N。
- Review 状态分布。
- 低置信度询盘列表。
- 失败 Agent Run 列表。

## 4. 数据来源

- PostgreSQL 中的 `inquiries`。
- `agent_results`。
- `agent_runs`。
- `agent_steps`。
- `review_logs`。
- AgentResult 中的 `retrieved_knowledge`。

## 5. 暂不做

- 不接 Prometheus / Grafana。
- 不做告警系统。
- 不做生产日志采集。
- 不做真实业务 KPI 承诺。
- 不用模拟指标夸大生产效果。

## 6. 后续验收标准

- API 能返回基础统计。
- 前端能展示 Evaluation Dashboard。
- 统计不影响 Agent 主流程。
- 文档明确这是 prototype evaluation，不代表生产准确率。
## A-Final 客服/业务员后台最终集成版

A-Final 已补齐客服/业务员后台闭环：Public Website Inquiry、Email Inquiry Import、Inquiry Console、Requirement Confirmation Card、Candidate Products、Reply Draft edit/copy/export、Human Review、Follow-up Status、Product Library Admin、Knowledge Upload、Qdrant Rebuild Index、Redis basic status integration。

当前边界保持不变：No automatic quotation, no stock commitment, no delivery commitment, no automatic email sending, manual review required。当前产品数据和知识库数据仍为高仿真模拟数据；项目定位仍是 portfolio / prototype 工程化项目，不代表完整生产系统。
