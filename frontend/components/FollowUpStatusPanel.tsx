"use client";

import { FormEvent, useState } from "react";
import { updateInquiryStatus } from "@/lib/api";
import { useI18n } from "@/lib/i18n";

const statuses = [
  "new",
  "analyzed",
  "need_clarification",
  "draft_ready",
  "reviewed",
  "followed_up",
  "closed",
  "lost"
];

export function FollowUpStatusPanel({
  inquiryId,
  currentStatus,
  onUpdated
}: {
  inquiryId: number;
  currentStatus: string;
  onUpdated?: () => void;
}) {
  const [status, setStatus] = useState(currentStatus);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const { language, statusText } = useI18n();
  const copy = language === "zh" ? zhCopy : enCopy;

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setSaving(true);
    setError("");
    setMessage("");
    try {
      await updateInquiryStatus(inquiryId, status);
      setMessage(copy.saved);
      onUpdated?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.failed);
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
      <h2 className="text-base font-semibold text-ink">{copy.title}</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600">{copy.description}</p>
      <form onSubmit={handleSubmit} className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-end">
        <label className="w-full max-w-sm space-y-1">
          <span className="text-sm font-medium text-slate-700">{copy.status}</span>
          <select
            value={status}
            onChange={(event) => setStatus(event.target.value)}
            className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
          >
            {statuses.map((item) => (
              <option key={item} value={item}>
                {statusText(item)}
              </option>
            ))}
          </select>
        </label>
        <button
          type="submit"
          disabled={saving}
          className="focus-ring rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
        >
          {saving ? copy.saving : copy.save}
        </button>
      </form>
      {message ? <div className="mt-3 rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-700">{message}</div> : null}
      {error ? <div className="mt-3 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div> : null}
    </section>
  );
}

const zhCopy = {
  title: "跟进状态 Follow-up Status",
  description: "用于业务员标记当前询盘跟进阶段；不会自动发送邮件或触发报价。",
  status: "状态",
  save: "保存状态",
  saving: "保存中...",
  saved: "跟进状态已更新。",
  failed: "更新跟进状态失败。"
};

const enCopy = {
  title: "Follow-up Status",
  description: "Mark the current inquiry follow-up stage. This does not send email or trigger quotation.",
  status: "Status",
  save: "Save Status",
  saving: "Saving...",
  saved: "Follow-up status updated.",
  failed: "Failed to update follow-up status."
};
