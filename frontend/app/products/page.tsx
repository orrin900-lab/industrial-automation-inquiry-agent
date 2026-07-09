"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { AuthGuard } from "@/components/AuthGuard";
import { createProduct, getProducts, updateProductStatus } from "@/lib/api";
import { useI18n } from "@/lib/i18n";
import type { ProductLibraryInput, ProductLibraryItem } from "@/lib/types";

const emptyProduct: ProductLibraryInput = {
  product_id: "",
  product_name: "",
  category: "PLC",
  brand: "",
  model: "",
  match_keywords: "",
  is_active: true
};

export default function ProductsPage() {
  return (
    <AuthGuard allowedRoles={["admin"]}>
      <ProductsPageContent />
    </AuthGuard>
  );
}

function ProductsPageContent() {
  const { language } = useI18n();
  const copy = language === "zh" ? zhCopy : enCopy;
  const [items, setItems] = useState<ProductLibraryItem[]>([]);
  const [category, setCategory] = useState("");
  const [query, setQuery] = useState("");
  const [activeOnly, setActiveOnly] = useState(false);
  const [providerNote, setProviderNote] = useState("");
  const [form, setForm] = useState<ProductLibraryInput>(emptyProduct);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadProducts = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const response = await getProducts({
        category,
        query,
        active_only: activeOnly,
        limit: 100
      });
      setItems(response.items || []);
      setProviderNote(response.provider_note);
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.loadFailed);
    } finally {
      setLoading(false);
    }
  }, [activeOnly, category, copy.loadFailed, query]);

  useEffect(() => {
    loadProducts();
  }, [loadProducts]);

  function updateField(field: keyof ProductLibraryInput, value: string | boolean) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleCreate(event: FormEvent) {
    event.preventDefault();
    if (!form.product_id.trim() || !form.product_name.trim() || !form.category.trim()) {
      setError(copy.required);
      return;
    }

    setSaving(true);
    setError("");
    setMessage("");
    try {
      await createProduct(form);
      setMessage(copy.saved);
      setForm(emptyProduct);
      await loadProducts();
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.saveFailed);
    } finally {
      setSaving(false);
    }
  }

  async function handleToggle(product: ProductLibraryItem) {
    setError("");
    setMessage("");
    try {
      await updateProductStatus(product.product_id, !product.is_active);
      setMessage(copy.statusUpdated);
      await loadProducts();
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.saveFailed);
    }
  }

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold text-ink">{copy.title}</h1>
        <p className="mt-2 max-w-4xl text-sm leading-6 text-slate-600">{copy.description}</p>
      </section>

      {providerNote ? (
        <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm leading-6 text-amber-800">
          {providerNote}
        </div>
      ) : null}

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <div className="grid gap-4 md:grid-cols-4">
          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">{copy.category}</span>
            <select
              value={category}
              onChange={(event) => setCategory(event.target.value)}
              className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
            >
              <option value="">{copy.allCategories}</option>
              <option value="PLC">PLC</option>
              <option value="VFD">VFD</option>
              <option value="HMI">HMI</option>
              <option value="Industrial Switch">Industrial Switch</option>
            </select>
          </label>
          <label className="space-y-1 md:col-span-2">
            <span className="text-sm font-medium text-slate-700">{copy.keyword}</span>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
              placeholder={copy.keywordPlaceholder}
            />
          </label>
          <label className="flex items-end gap-2 text-sm text-slate-700">
            <input
              type="checkbox"
              checked={activeOnly}
              onChange={(event) => setActiveOnly(event.target.checked)}
            />
            {copy.activeOnly}
          </label>
        </div>
      </section>

      {error ? <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div> : null}
      {message ? <div className="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">{message}</div> : null}

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <h2 className="text-base font-semibold text-ink">{copy.listTitle}</h2>
        <div className="mt-4 overflow-x-auto rounded-md border border-line">
          <table className="min-w-full divide-y divide-line text-sm">
            <thead className="bg-panel text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-3 py-2">product_id</th>
                <th className="px-3 py-2">{copy.name}</th>
                <th className="px-3 py-2">{copy.category}</th>
                <th className="px-3 py-2">brand</th>
                <th className="px-3 py-2">model</th>
                <th className="px-3 py-2">{copy.active}</th>
                <th className="px-3 py-2">{copy.action}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line bg-white">
              {items.map((item) => (
                <tr key={item.product_id}>
                  <td className="px-3 py-3 font-mono text-xs text-slate-600">{item.product_id}</td>
                  <td className="px-3 py-3 font-medium text-ink">{item.product_name}</td>
                  <td className="px-3 py-3 text-slate-700">{item.category}</td>
                  <td className="px-3 py-3 text-slate-700">{item.brand || "-"}</td>
                  <td className="px-3 py-3 text-slate-700">{item.model || "-"}</td>
                  <td className="px-3 py-3 text-slate-700">{item.is_active ? copy.yes : copy.no}</td>
                  <td className="px-3 py-3">
                    <button
                      type="button"
                      onClick={() => handleToggle(item)}
                      className="focus-ring rounded-md border border-line px-3 py-1 text-xs font-semibold text-slate-700"
                    >
                      {item.is_active ? copy.deactivate : copy.activate}
                    </button>
                  </td>
                </tr>
              ))}
              {!items.length ? (
                <tr>
                  <td colSpan={7} className="px-3 py-6 text-center text-slate-500">
                    {loading ? copy.loading : copy.empty}
                  </td>
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>
      </section>

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <h2 className="text-base font-semibold text-ink">{copy.createTitle}</h2>
        <form onSubmit={handleCreate} className="mt-4 grid gap-4 md:grid-cols-2">
          <Field label="product_id" value={form.product_id} onChange={(value) => updateField("product_id", value)} />
          <Field label={copy.name} value={form.product_name} onChange={(value) => updateField("product_name", value)} />
          <Field label={copy.category} value={form.category} onChange={(value) => updateField("category", value)} />
          <Field label="brand" value={String(form.brand || "")} onChange={(value) => updateField("brand", value)} />
          <Field label="model" value={String(form.model || "")} onChange={(value) => updateField("model", value)} />
          <Field label="match_keywords" value={String(form.match_keywords || "")} onChange={(value) => updateField("match_keywords", value)} />
          <label className="flex items-end gap-2 text-sm text-slate-700">
            <input
              type="checkbox"
              checked={form.is_active !== false}
              onChange={(event) => updateField("is_active", event.target.checked)}
            />
            {copy.active}
          </label>
          <div className="flex items-end justify-end">
            <button
              type="submit"
              disabled={saving}
              className="focus-ring rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
            >
              {saving ? copy.saving : copy.create}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}

function Field({
  label,
  value,
  onChange
}: {
  label: string;
  value?: string | null;
  onChange: (value: string) => void;
}) {
  return (
    <label className="space-y-1">
      <span className="text-sm font-medium text-slate-700">{label}</span>
      <input
        value={value || ""}
        onChange={(event) => onChange(event.target.value)}
        className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
      />
    </label>
  );
}

const zhCopy = {
  title: "产品库管理 Product Library Admin",
  description: "轻量产品库管理页面，仅 admin 可访问。当前用于 demo 产品资料查看、搜索、新增和启用/停用，不代表已接入真实 ERP。",
  category: "产品类别",
  allCategories: "全部类别",
  keyword: "关键词",
  keywordPlaceholder: "搜索 product_id / name / brand / model",
  activeOnly: "只看启用产品",
  listTitle: "产品列表",
  name: "产品名称",
  active: "启用状态",
  action: "操作",
  yes: "是",
  no: "否",
  activate: "启用",
  deactivate: "停用",
  loading: "加载中...",
  empty: "暂无产品",
  createTitle: "新增 / 覆盖 demo 产品",
  create: "保存产品",
  saving: "保存中...",
  saved: "产品已保存。",
  statusUpdated: "产品状态已更新。",
  required: "product_id、产品名称和类别必填。",
  loadFailed: "加载产品失败。",
  saveFailed: "保存产品失败。"
};

const enCopy = {
  title: "Product Library Admin",
  description: "A lightweight admin-only product library page for demo product viewing, search, creation, and activation status. It does not indicate a real ERP integration.",
  category: "Category",
  allCategories: "All categories",
  keyword: "Keyword",
  keywordPlaceholder: "Search product_id / name / brand / model",
  activeOnly: "Active only",
  listTitle: "Product List",
  name: "Product Name",
  active: "Active",
  action: "Action",
  yes: "Yes",
  no: "No",
  activate: "Activate",
  deactivate: "Deactivate",
  loading: "Loading...",
  empty: "No products found.",
  createTitle: "Create / Replace Demo Product",
  create: "Save Product",
  saving: "Saving...",
  saved: "Product saved.",
  statusUpdated: "Product status updated.",
  required: "product_id, product name and category are required.",
  loadFailed: "Failed to load products.",
  saveFailed: "Failed to save product."
};
