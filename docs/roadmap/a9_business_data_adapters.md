# A9 真实业务数据接口预留 Business Data Adapter Layer

## 1. 阶段目标

A9 目标是规划真实业务数据接入抽象，让当前 CSV / Markdown demo 数据能够平滑迁移到数据库、ERP、CRM 或邮件来源。

本阶段只做路线图和技术设计，不开发代码。

## 2. ProductDataProvider 抽象

建议定义统一产品数据接口：

```text
ProductDataProvider
- list_products()
- get_product_by_id(product_id)
- search_products(filters)
```

候选实现：

- `CSVProductProvider`：保留当前 `products.csv` demo 数据。
- `DatabaseProductProvider`：预留 PostgreSQL 产品表读取。
- `ERPProductProvider`：预留 ERP API 或导出文件接入。

## 3. InquirySourceProvider 抽象

建议定义统一询盘来源接口：

```text
InquirySourceProvider
- list_inquiries()
- get_inquiry(source_id)
- normalize_inquiry(raw_payload)
```

候选实现：

- `WebsiteInquiryProvider`：官网表单询盘。
- `EmailInquiryProvider`：邮件询盘导入。
- `ManualInquiryProvider`：业务员手动录入。

## 4. 设计原则

- API 层不直接读取 CSV / ERP。
- Agent Core 只依赖 Repository / Provider 接口。
- 保留现有 fallback demo 数据。
- 真实企业数据接入前必须做字段映射和权限评估。

## 5. 暂不做

- 不接真实 ERP。
- 不接真实 CRM。
- 不导入真实客户数据。
- 不改变现有 PostgreSQL 主模型。
- 不做数据同步任务。

## 6. 后续验收标准

- 文档明确 provider 抽象和实现边界。
- 不破坏现有 ProductRepository。
- 后续 A9 实现时应保留 CSV fallback。

## 7. A9 实施结果

A9 已完成轻量数据适配层实现：

- `backend/app/data_providers/product_provider.py`
- `backend/app/data_providers/csv_product_provider.py`
- `backend/app/data_providers/database_product_provider.py`
- `backend/app/data_providers/erp_product_provider.py`
- `backend/app/data_providers/inquiry_source_provider.py`
- `backend/app/data_providers/manual_inquiry_provider.py`
- `backend/app/data_providers/website_inquiry_provider.py`
- `backend/app/data_providers/email_inquiry_provider.py`

当前默认配置：

```env
PRODUCT_PROVIDER=csv
INQUIRY_SOURCE_PROVIDER=manual
```

reserved provider 当前仅作为未来接口骨架，不接真实 ERP、CRM、邮箱或数据库产品表。测试覆盖 provider fallback、manual normalize、`/analyze` 回归、auth 和 knowledge 回归。
