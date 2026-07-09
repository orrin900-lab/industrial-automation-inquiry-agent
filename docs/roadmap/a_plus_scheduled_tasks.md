# A+ Scheduled Tasks

## Purpose

本文件记录 A+ 阶段可后续安排的开发任务，不代表已经自动执行。

## Suggested Order

1. A8 Auth & Roles
2. A8.5 Auth stabilization
3. A9 Business Data Adapter Layer
4. A10 Email Inquiry Import Enhancement
5. A11 Evaluation & Monitoring Enhancement

## Safety Rules

- 每个阶段先建 feature 分支。
- 每个阶段必须有测试和文档。
- 测试失败不合并。
- merge 冲突不强行处理。
- GitHub push 失败不强推。
- 不删除用户文件。
- 不接真实 API Key。
- 不自动报价。
- 不承诺库存。
- 不承诺交期。
- 不自动发送邮件。

## Future Automation Candidate

如果后续需要自动化，可拆成独立 Codex 任务，而不是一次性扩大范围：

- A8 implementation only。
- A8.5 stabilization only。
- A9 adapter implementation only。
- A10 email import implementation only。
- A11 evaluation dashboard only。

