# 项目难点与解决方案 Project Challenges

## 1. 模糊英文询盘结构化

问题描述：客户询盘通常是自然语言，信息不完整，可能只描述产品大类或应用场景。  
解决方案：设计 `InquiryInput` 和 `AgentResult`，通过 Agent Workflow 拆分意图识别、品类判断、需求抽取和缺失信息检查。  
面试表达：我没有让模型直接自由回答，而是把结果固定为结构化 JSON，便于前端展示、数据库保存和人工复核。  
可继续优化方向：引入更强的 LLM extraction、few-shot prompt、标注数据集和抽取准确率评测。

## 2. 工业产品参数抽取

问题描述：PLC、VFD、HMI、Industrial Switch 的关键参数不同，不能用一套字段粗暴处理。  
解决方案：按产品类别设计 technical_specs，如 PLC 的 I/O、输出类型、供电和通信，VFD 的功率、电压、相数和控制模式。  
面试表达：工业品询盘的价值在参数确认，不只是问答，所以我把参数抽取做成类别相关结构。  
可继续优化方向：增加更多产品线、参数单位归一化、型号解析和品牌兼容性校验。

## 3. 候选产品匹配

问题描述：不能让 Agent 凭空推荐产品，否则会产生业务风险。  
解决方案：候选产品只能来自 `products.csv`，通过 ProductRepository 读取，再由 ProductMatcher 根据类别、关键词和参数评分。  
面试表达：我把产品推荐限定在产品库内，保证推荐有数据来源，避免模型幻觉。  
可继续优化方向：接入真实 PIM/ERP，增加库存、认证、价格权限和人工确认流程。

## 4. RAG 检索稳定性

问题描述：轻量 keyword RAG 在语义匹配上有限，真实知识库规模变大后可维护性差。  
解决方案：A6 引入 Qdrant-based Vector Retrieval，把 Markdown chunks 写入 Qdrant，并保持 `retrieved_knowledge` 结构兼容。  
面试表达：我从 keyword RAG 升级到 Qdrant RAG，同时没有破坏前端展示结构。  
可继续优化方向：使用 OpenAI embeddings、sentence-transformers、bge-m3、rerank 和召回率评测。

## 5. Qdrant 不可用 fallback

问题描述：如果 Qdrant 没启动或 collection 异常，Agent 分析不能整体失败。  
解决方案：Retriever 捕获 Qdrant 异常，自动 fallback 到 keyword retriever，并在 Agent Trace 中记录 `keyword_fallback`。  
面试表达：我把 fallback 作为工程稳定性设计，而不是只追求理想路径。  
可继续优化方向：增加重试、健康检查、告警、后台 rebuild 状态和降级日志。

## 6. Agent Trace 可观测性

问题描述：AI Agent 如果只返回结论，业务员和开发者很难判断结果来源。  
解决方案：记录每个节点的 step_name、mode、success、latency_ms 和 output_summary，并在前端展示。  
面试表达：Agent Trace 让系统从黑盒变成可观测流程，便于 debug 和业务复核。  
可继续优化方向：增加 trace 搜索、失败聚合、耗时分析和可视化链路图。

## 7. 不自动报价的业务边界

问题描述：工业品报价涉及供应链、价格策略、库存和付款条款，自动报价风险高。  
解决方案：Prompt、风险检查和前端文案都明确不自动报价、不承诺库存、不承诺交期。Review 只保存人工审核状态。  
面试表达：我把项目定位成需求确认和转化辅助，而不是自动成交系统。  
可继续优化方向：未来若接报价系统，需要引入权限、审批、ERP 价格策略和审计记录。

## 8. 前后端类型结构对齐

问题描述：AgentResult 字段较多，前后端结构不一致会导致页面展示和 API 调用出错。  
解决方案：后端使用 Pydantic schema，前端使用 TypeScript types，API client 集中封装在 `frontend/lib/api.ts`。  
面试表达：我没有在页面里散写 fetch，而是用统一 API client 和类型定义保持结构一致。  
可继续优化方向：用 OpenAPI 自动生成 TypeScript client，减少手写类型维护成本。

## 9. Docker Compose 多服务联调

问题描述：frontend、backend、PostgreSQL、Qdrant 多服务联调容易出现端口、CORS、网络和启动顺序问题。  
解决方案：Docker Compose 中配置 depends_on、healthcheck、端口映射和环境变量，前端浏览器访问宿主机 backend 地址。  
面试表达：我把项目从本地命令启动推进到 Docker Compose 一键启动，方便复测和展示。  
可继续优化方向：生产环境可增加 Nginx、HTTPS、Alembic、日志系统和 CI/CD。

## 10. 作品集项目与生产系统边界

问题描述：求职展示需要体现工程能力，但不能夸大为真实生产上线。  
解决方案：README、docs、manual test report 和 career package 都明确说明模拟数据、prototype、未接真实企业系统。  
面试表达：我会清楚说明这是工程化作品集项目，但它覆盖了生产系统需要考虑的关键接口和边界。  
可继续优化方向：如果进入真实企业场景，需要做数据治理、权限、审计、监控和安全评估。

