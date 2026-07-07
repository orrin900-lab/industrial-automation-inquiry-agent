"use client";

import type { ProductCandidate } from "@/lib/types";
import { formatPercent } from "@/lib/format";
import { useI18n } from "@/lib/i18n";

export function CandidateProducts({ products }: { products: ProductCandidate[] }) {
  const { t } = useI18n();

  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
      <h2 className="text-base font-semibold text-ink">{t("products.title")}</h2>
      {!products.length ? (
        <p className="mt-3 text-sm text-slate-500">{t("products.empty")}</p>
      ) : (
        <div className="mt-4 grid gap-3">
          {products.map((product) => (
            <article key={product.product_id} className="rounded-md border border-line bg-panel p-4">
              <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <div className="font-semibold text-ink">{product.product_name}</div>
                  <div className="text-sm text-slate-500">
                    {product.product_id} · {product.category}
                  </div>
                </div>
                <div className="rounded-md bg-white px-2 py-1 text-sm font-semibold text-accent">
                  {formatPercent(product.match_score)}
                </div>
              </div>
              <p className="mt-3 text-sm leading-6 text-slate-700">{product.match_reason}</p>
              {product.missing_confirmations?.length ? (
                <div className="mt-3">
                  <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">{t("products.missingConfirmations")}</div>
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-700">
                    {product.missing_confirmations.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
