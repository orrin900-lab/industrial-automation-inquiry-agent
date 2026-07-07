"use client";

import { useI18n } from "@/lib/i18n";

export function MissingInfoPanel({ items }: { items: string[] }) {
  const { t } = useI18n();

  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
      <h2 className="text-base font-semibold text-ink">{t("missing.title")}</h2>
      {!items.length ? (
        <p className="mt-3 text-sm text-slate-500">{t("missing.empty")}</p>
      ) : (
        <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-slate-700">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      )}
    </section>
  );
}
