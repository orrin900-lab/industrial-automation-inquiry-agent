"use client";

import { useI18n } from "@/lib/i18n";

export function ReplyDraftEditor({
  value,
  onChange,
  fileName = "reply_draft.md"
}: {
  value: string;
  onChange: (value: string) => void;
  fileName?: string;
}) {
  const { t } = useI18n();

  async function handleCopy() {
    await navigator.clipboard.writeText(value);
  }

  function handleExport() {
    const markdown = [
      "# English Reply Draft",
      "",
      "> Draft only. Manual review required. No automatic quotation, stock commitment, delivery commitment, or automatic email sending.",
      "",
      value
    ].join("\n");
    const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h2 className="text-base font-semibold text-ink">{t("reply.title")}</h2>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={handleCopy}
            className="focus-ring rounded-md border border-line px-3 py-2 text-xs font-semibold text-slate-700"
          >
            Copy Reply
          </button>
          <button
            type="button"
            onClick={handleExport}
            className="focus-ring rounded-md border border-line px-3 py-2 text-xs font-semibold text-slate-700"
          >
            Export Markdown
          </button>
        </div>
      </div>
      <textarea
        value={value}
        onChange={(event) => onChange(event.target.value)}
        rows={9}
        className="focus-ring mt-4 w-full rounded-md border border-line bg-white px-3 py-2 text-sm leading-6"
      />
      <p className="mt-2 text-xs text-slate-500">
        {t("reply.note")}
      </p>
    </section>
  );
}
