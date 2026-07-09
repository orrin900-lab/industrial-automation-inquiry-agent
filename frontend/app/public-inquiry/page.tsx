"use client";

import { FormEvent, useState } from "react";
import { submitPublicInquiry } from "@/lib/api";
import { useI18n } from "@/lib/i18n";
import type { PublicInquiryInput } from "@/lib/types";

const initialForm: PublicInquiryInput = {
  name: "",
  email: "",
  company: "",
  country: "",
  product_category: "",
  message: ""
};

export default function PublicInquiryPage() {
  const { language } = useI18n();
  const copy = language === "zh" ? zhCopy : enCopy;
  const [form, setForm] = useState<PublicInquiryInput>(initialForm);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  function update(field: keyof PublicInquiryInput, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!form.name.trim() || !form.email.trim() || !form.message.trim()) {
      setError(copy.required);
      return;
    }

    setSubmitting(true);
    setError("");
    setMessage("");
    try {
      const response = await submitPublicInquiry(form);
      setMessage(`${copy.success} #${response.inquiry.id}`);
      setForm(initialForm);
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.failed);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <section className="rounded-lg border border-line bg-white p-6 shadow-subtle">
        <h1 className="text-2xl font-semibold text-ink">{copy.title}</h1>
        <p className="mt-2 text-sm leading-6 text-slate-600">{copy.description}</p>
      </section>

      <form onSubmit={handleSubmit} className="space-y-5 rounded-lg border border-line bg-white p-6 shadow-subtle">
        <div className="grid gap-4 md:grid-cols-2">
          <Field label={copy.name} value={form.name} onChange={(value) => update("name", value)} required />
          <Field label={copy.email} value={form.email} onChange={(value) => update("email", value)} required />
          <Field label={copy.company} value={form.company || ""} onChange={(value) => update("company", value)} />
          <Field label={copy.country} value={form.country || ""} onChange={(value) => update("country", value)} />
        </div>

        <label className="space-y-1">
          <span className="text-sm font-medium text-slate-700">{copy.category}</span>
          <select
            value={form.product_category || ""}
            onChange={(event) => update("product_category", event.target.value)}
            className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
          >
            <option value="">{copy.notSure}</option>
            <option value="PLC">PLC</option>
            <option value="VFD">VFD</option>
            <option value="HMI">HMI</option>
            <option value="Industrial Switch">Industrial Switch</option>
          </select>
        </label>

        <label className="space-y-1">
          <span className="text-sm font-medium text-slate-700">{copy.message}</span>
          <textarea
            value={form.message}
            onChange={(event) => update("message", event.target.value)}
            rows={8}
            className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm leading-6"
            placeholder={copy.placeholder}
            required
          />
        </label>

        <div className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm leading-6 text-amber-800">
          {copy.boundary}
        </div>

        {message ? <div className="rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-700">{message}</div> : null}
        {error ? <div className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div> : null}

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={submitting}
            className="focus-ring rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
          >
            {submitting ? copy.submitting : copy.submit}
          </button>
        </div>
      </form>
    </div>
  );
}

function Field({
  label,
  value,
  onChange,
  required
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
}) {
  return (
    <label className="space-y-1">
      <span className="text-sm font-medium text-slate-700">{label}</span>
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
        required={required}
      />
    </label>
  );
}

const zhCopy = {
  title: "官网询盘入口 Public Website Inquiry",
  description: "模拟官网询盘表单。客户无需登录即可提交需求，后台客服或业务员后续人工分析与跟进。",
  name: "Name / 姓名",
  email: "Email / 邮箱",
  company: "Company / 公司",
  country: "Country / 国家",
  category: "Product Category / 产品类别",
  notSure: "Not sure / 不确定",
  message: "Message / 询盘内容",
  placeholder: "Please describe the product, quantity, technical parameters and application.",
  boundary: "Demo boundary: no automatic quotation, no stock commitment, no delivery commitment, and no automatic email sending. Manual review is required.",
  submit: "Submit Inquiry",
  submitting: "Submitting...",
  success: "Inquiry submitted successfully. Inquiry ID:",
  failed: "Failed to submit inquiry.",
  required: "Name, email and message are required."
};

const enCopy = {
  title: "Public Website Inquiry",
  description: "A lightweight demo website inquiry form. Customers can submit needs without signing in; sales/support users review and follow up manually.",
  name: "Name",
  email: "Email",
  company: "Company",
  country: "Country",
  category: "Product Category",
  notSure: "Not sure",
  message: "Message",
  placeholder: "Please describe the product, quantity, technical parameters and application.",
  boundary: "Demo boundary: no automatic quotation, no stock commitment, no delivery commitment, and no automatic email sending. Manual review is required.",
  submit: "Submit Inquiry",
  submitting: "Submitting...",
  success: "Inquiry submitted successfully. Inquiry ID:",
  failed: "Failed to submit inquiry.",
  required: "Name, email and message are required."
};
