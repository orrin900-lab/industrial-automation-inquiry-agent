# 技术追问 Q&A Technical Interview Q&A

回答原则：真实、专业、不夸大。明确说明该项目是 portfolio / prototype 工程化项目，使用高仿真模拟数据，不是完整生产系统。

## 1. 为什么选择工业自动化外贸询盘场景？

因为这个场景和我的行业背景有自然连接。工业自动化询盘不是简单客服问答，里面有产品类别、型号、技术参数、应用场景和商务风险。用 AI Agent 做需求确认，比泛化聊天机器人更能体现业务理解和工程落地能力。

## 2. Agent Workflow 怎么设计？

我把流程拆成多个节点：意图识别、产品类别判断、需求抽取、缺失信息检查、知识库检索、候选产品匹配、英文回复草稿、风险检查。每个节点写入结构化状态，最终输出 `AgentResult`，并保留 `Agent Trace`。

## 3. RAG 在项目里解决什么问题？

RAG 用来让 Agent 的回复和判断参考可追溯知识来源，包括 FAQ、选型规则和邮件模板。这样不是让模型凭空回答，而是返回 `Retrieved Knowledge`，业务员能看到参考了哪些知识片段。

## 4. 为什么用 Qdrant？

Qdrant 是轻量、易部署的向量数据库，适合 Docker Compose 本地演示，也方便后续生产化扩展。它支持 collection、points、payload 和向量检索，能把 Markdown chunks 和 metadata 保存起来。

## 5. 为什么保留 Keyword Fallback？

因为作品集和企业系统都需要降级能力。Qdrant 可能没启动、collection 可能没建好、网络可能失败。如果没有 fallback，Agent 分析链路会直接失败。Keyword Fallback 保证 demo 和基本业务流程仍可运行。

## 6. deterministic hashing embedding 是什么？

它是一种本地、确定性的轻量 embedding。系统把文本 token hash 到固定维度，例如 384 维，再做 L2 normalize。它不是生产级语义 embedding，但能避免 API Key 和模型下载依赖，适合 prototype 稳定演示。

## 7. 为什么不用 OpenAI embedding？

因为这个项目需要保证无 API Key 也能运行。OpenAI embedding 更适合生产级语义检索，但会带来密钥、网络、费用和稳定性依赖。我在接口上保留了替换空间，后续可以接 OpenAI embeddings 或 sentence-transformers。

## 8. 当前 RAG 是否生产级？

不是完整生产级。当前 Qdrant RAG 已具备工程接口、payload metadata、fallback 和 Knowledge Base Admin，但 embedding 是 prototype 方案，知识库规模也较小。生产级还需要更好的 embedding、评测集、权限、增量更新和监控。

## 9. 如何升级到生产级 RAG？

可以替换为 OpenAI embeddings、bge-m3 或 sentence-transformers；增加 chunk 策略评估、召回率测试、rerank、知识库版本管理、增量索引、权限控制、监控和人工标注评测集。

## 10. Agent Trace 有什么作用？

Agent Trace 记录每个节点的 step_name、mode、success、latency 和 output_summary。它能帮助业务员和开发者理解 Agent 的判断过程，也能排查 LLM fallback、Qdrant fallback 或规则节点异常。

## 11. Human-in-the-loop 为什么重要？

工业品外贸涉及报价、库存、交期、品牌兼容性和认证风险。如果系统自动发送最终回复，风险很高。Human-in-the-loop 让 AI 只做辅助分析和草稿生成，最终由业务员审核。

## 12. 为什么不自动报价？

报价涉及成本、数量、供应链、运输、付款条件和客户等级。当前系统定位是 quotation preparation 前的需求确认，不适合自动报价。自动报价必须接入真实 ERP、库存、价格策略和审批流程。

## 13. 为什么不承诺库存和交期？

库存和交期变化快，需要实时供应链系统确认。当前项目没有接 ERP/WMS，也没有真实库存数据，所以只能提示业务员人工确认，不能由 Agent 承诺。

## 14. PostgreSQL 存了什么？

PostgreSQL 保存 inquiries、agent_results、agent_runs、agent_steps 和 review_logs。这样可以追踪询盘来源、Agent 分析结果、执行轨迹和人工审核记录。

## 15. Qdrant 存了什么？

Qdrant 存 Markdown 知识库 chunks 的向量和 payload。payload 包括 content、source_file、section_title、document_type 和 chunk_id。前端 Retrieved Knowledge 和 Knowledge Base Admin 都依赖这些结构。

## 16. Docker Compose 如何设计？

Compose 包含 postgres、qdrant、backend、frontend 四个服务。backend 依赖 PostgreSQL 和 Qdrant，frontend 依赖 backend healthcheck。宿主机访问 frontend `3001`、backend `8000`、Qdrant `6333`。

## 17. 前后端如何交互？

前端通过 `frontend/lib/api.ts` 统一封装 API 调用，包括 analyze、inquiry list/detail、review、samples 和 knowledge APIs。后端返回结构化 JSON，前端用 TypeScript types 对齐。

## 18. Bilingual UI 为什么要做？

这个项目面向中文求职展示和英文外贸业务场景。业务员后台可以中文展示，英文回复草稿保持英文。Bilingual UI 也说明前端状态管理和文案抽象能力。

## 19. Knowledge Base Admin 有什么作用？

它让 RAG 不再是黑盒。用户可以查看 Qdrant 是否可用、collection 名称、points_count、embedding provider、chunks 列表和 source_file 筛选，并手动 rebuild index。

## 20. 这个项目的最大难点是什么？

难点是把业务场景拆成可靠的工程链路：从模糊询盘到结构化需求，再到 RAG、产品匹配、风险控制、人工审核和持久化。不是单个模型调用，而是一个端到端系统。

## 21. 你如何保证 fallback 稳定？

我设计了多层 fallback：没有 LLM API Key 时使用规则抽取；Qdrant 不可用时使用 keyword retriever；Agent Trace 会记录 fallback mode；测试覆盖了 Qdrant unavailable 和无 LLM 的场景。

## 22. 如果 Qdrant 挂了怎么办？

Retriever 捕获 Qdrant 异常后切换到 keyword fallback，`AgentResult.retrieved_knowledge` 结构不变，前端仍能展示结果。系统不会因为 Qdrant 不可用导致 analyze 整体失败。

## 23. 如果 LLM 不稳定怎么办？

当前 LLM 是可选能力。LLM 不可用、没有 API Key、返回非法 JSON 时，系统回退到规则抽取和模板回复，保证 demo 和基础流程可运行。

## 24. 这个项目如何接入真实企业数据？

需要替换模拟产品库，接入真实 PIM/ERP/CRM 数据；建立知识库同步机制；增加权限、审计、数据脱敏和审批；报价、库存、交期必须接真实系统并加入人工审批。

## 25. 下一步怎么扩展？

短期可以增强 Knowledge Base Admin，例如 rebuild 日志、collection diagnostics、chunk preview。中期可以接生产级 embedding、rerank、权限和知识库上传。长期可以接 CRM/ERP/邮件系统，但仍保留人工审核。

## 26. 为什么不用 LangChain 或 LangGraph 深度框架？

当前重点是可控的工程闭环和业务边界，直接用轻量 Agent Core 更容易控制结构化输出、fallback 和测试。后续如果流程复杂，可以引入 LangGraph 做状态图和节点编排。

## 27. Candidate Products 如何避免凭空生成？

候选产品必须来自 `products.csv`，通过 ProductRepository 读取。ProductMatcher 根据产品类别、关键词和 technical_specs 打分，不允许 Agent 节点凭空编造产品。

## 28. 这个项目如何体现工程化？

它不只是一个 demo 页面。项目有 FastAPI API、Pydantic schema、Repository、PostgreSQL、Qdrant、Docker Compose、Next.js 前端、pytest、manual test report、screenshots 和 GitHub 发布材料。

## 29. 当前最不完善的地方是什么？

RAG 的 embedding 还不是生产级语义模型，数据也是模拟数据，没有接真实企业系统，也没有登录权限和审计流程。这些是后续生产化方向。

## 30. 如果面试官说这只是作品集项目，你怎么回答？

我会承认它是 portfolio / prototype 项目，不是生产系统。但它展示了从业务建模、Agent Workflow、RAG、持久化、前端后台、Docker 部署到风险边界的完整工程思路，适合证明我具备 AI 应用开发能力。

## A-Final 追加追问

### 31. A-Final 和前面的版本相比补齐了什么？

A-Final 不只是分析接口，而是补齐了客服 / 业务员后台闭环：Public Inquiry、Email Inquiry Import、Inquiry List、Inquiry Detail、Requirement Confirmation Card、Reply Draft edit/copy/export、Human Review、Follow-up Status、Product Library Admin、Knowledge Upload、Redis status 和 Docker Compose 五服务启动。

### 32. Product Library Admin 是真实 ERP 吗？

不是。当前是 demo product library，用来展示后台产品管理入口和 provider layer 的扩展方向。真实生产中可以把 `CSVProductProvider` 替换成数据库产品表或 ERP adapter，但当前没有接入真实 ERP、库存或报价系统。

### 33. Knowledge Upload 是否等同完整知识库管理系统？

不是。当前只允许 admin 上传 `.md` 文件并手动 rebuild Qdrant index，不支持在线编辑、删除、审批流或版本管理。它是 prototype 级知识库运维入口。

### 34. Redis 在项目中做了什么？

A-Final 只做 Redis 基础接入和 system status 展示，用于预留缓存、限流或后台任务状态能力。当前没有引入 Celery、复杂队列、分布式锁或异步任务系统。

### 35. 为什么 Reply Draft 只支持复制和导出，不自动发送？

工业品外贸回复涉及价格、库存、交期、兼容性和商务条款。系统只生成草稿并支持复制 / Markdown 导出，最终必须由业务员人工审核后通过正式渠道发送，避免自动承诺风险。
