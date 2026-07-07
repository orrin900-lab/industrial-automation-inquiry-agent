"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import type { InquiryInput, SampleInquiry } from "@/lib/types";
import { getSampleInquiries } from "@/lib/api";
import { useI18n } from "@/lib/i18n";

const emptyForm: InquiryInput = {
  channel: "website",
  customer_name: "",
  customer_email: "",
  company: "",
  country: "",
  subject: "",
  message: "",
  attachments: []
};

type InquiryTextField =
  | "channel"
  | "customer_name"
  | "customer_email"
  | "company"
  | "country"
  | "subject"
  | "message";

export function InquiryForm({
  onSubmit,
  submitting
}: {
  onSubmit: (payload: InquiryInput) => Promise<void>;
  submitting?: boolean;
}) {
  const [form, setForm] = useState<InquiryInput>(emptyForm);
  const [samples, setSamples] = useState<SampleInquiry[]>([]);
  const [selectedSample, setSelectedSample] = useState("");
  const [sampleError, setSampleError] = useState("");
  const [formError, setFormError] = useState("");
  const { t } = useI18n();

  useEffect(() => {
    let mounted = true;

    getSampleInquiries()
      .then((payload) => {
        if (mounted) {
          setSamples(payload.samples || []);
        }
      })
      .catch(() => {
        if (mounted) {
          setSampleError(t("form.sampleUnavailable"));
        }
      });

    return () => {
      mounted = false;
    };
  }, [t]);

  const sampleOptions = useMemo(
    () =>
      samples.map((sample, index) => ({
        value: String(sample.id || index),
        label: `${sample.expected_category || sample.subject || "Sample"}`
      })),
    [samples]
  );

  function updateField(field: InquiryTextField, value: string) {
    setForm((current) => ({
      ...current,
      [field]: value
    }));
  }

  function loadSample(value: string) {
    setSelectedSample(value);
    const sample = samples.find((item, index) => String(item.id || index) === value);
    if (!sample) {
      return;
    }

    setForm({
      channel: sample.channel || "website",
      customer_name: sample.customer_name || "",
      customer_email: sample.customer_email || "",
      company: sample.company || "",
      country: sample.country || "",
      subject: sample.subject || `${sample.expected_category || "Product"} inquiry`,
      message: sample.message,
      attachments: []
    });
    setFormError("");
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!form.message.trim()) {
      setFormError(t("form.messageRequired"));
      return;
    }

    setFormError("");
    await onSubmit({
      ...form,
      attachments: []
    });
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5 rounded-lg border border-line bg-white p-5 shadow-subtle">
      <div className="grid gap-4 md:grid-cols-2">
        <label className="space-y-1">
          <span className="text-sm font-medium text-slate-700">{t("form.loadSample")}</span>
          <select
            value={selectedSample}
            onChange={(event) => loadSample(event.target.value)}
            className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
          >
            <option value="">{t("form.manualInput")}</option>
            {sampleOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <label className="space-y-1">
          <span className="text-sm font-medium text-slate-700">{t("form.channel")}</span>
          <select
            value={form.channel}
            onChange={(event) => updateField("channel", event.target.value)}
            className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
          >
            <option value="website">{t("form.websiteInquiry")}</option>
            <option value="email">{t("form.emailInquiry")}</option>
          </select>
        </label>
      </div>

      {sampleError ? <div className="rounded-md bg-amber-50 px-3 py-2 text-sm text-warn">{sampleError}</div> : null}
      {formError ? <div className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{formError}</div> : null}

      <div className="grid gap-4 md:grid-cols-2">
        <Field label={t("form.customerName")} value={form.customer_name || ""} onChange={(value) => updateField("customer_name", value)} />
        <Field label={t("form.customerEmail")} value={form.customer_email || ""} onChange={(value) => updateField("customer_email", value)} />
        <Field label={t("form.company")} value={form.company || ""} onChange={(value) => updateField("company", value)} />
        <Field label={t("form.country")} value={form.country || ""} onChange={(value) => updateField("country", value)} />
      </div>

      <Field label={t("form.subject")} value={form.subject || ""} onChange={(value) => updateField("subject", value)} />

      <label className="space-y-1">
        <span className="text-sm font-medium text-slate-700">{t("form.message")}</span>
        <textarea
          value={form.message}
          onChange={(event) => updateField("message", event.target.value)}
          rows={7}
          className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm leading-6"
          placeholder={t("form.messagePlaceholder")}
        />
      </label>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={submitting}
          className="focus-ring rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
        >
          {submitting ? t("form.analyzing") : t("form.submit")}
        </button>
      </div>
    </form>
  );
}

function Field({
  label,
  value,
  onChange
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="space-y-1">
      <span className="text-sm font-medium text-slate-700">{label}</span>
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
      />
    </label>
  );
}
