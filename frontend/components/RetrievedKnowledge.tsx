"use client";

import type { RetrievedKnowledge as RetrievedKnowledgeItem } from "@/lib/types";
import { truncate } from "@/lib/format";
import { useI18n } from "@/lib/i18n";

export function RetrievedKnowledge({ items }: { items: RetrievedKnowledgeItem[] }) {
  const { t } = useI18n();

  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
      <h2 className="text-base font-semibold text-ink">{t("knowledge.title")}</h2>
      {!items.length ? (
        <p className="mt-3 text-sm text-slate-500">{t("knowledge.empty")}</p>
      ) : (
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full divide-y divide-line text-sm">
            <thead className="bg-panel text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-3 py-2">{t("knowledge.source")}</th>
                <th className="px-3 py-2">{t("knowledge.section")}</th>
                <th className="px-3 py-2">{t("knowledge.score")}</th>
                <th className="px-3 py-2">{t("knowledge.preview")}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {items.slice(0, 5).map((item, index) => (
                <tr key={`${item.metadata?.source_file || "source"}-${index}`}>
                  <td className="px-3 py-2">{item.metadata?.source_file || "-"}</td>
                  <td className="px-3 py-2">{item.metadata?.section_title || "-"}</td>
                  <td className="px-3 py-2">{Number.isFinite(item.score) ? item.score.toFixed(2) : "-"}</td>
                  <td className="max-w-xl px-3 py-2 text-slate-600">{truncate(item.content || "", 180)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
