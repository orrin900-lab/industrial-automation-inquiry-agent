"use client";

import type { AgentResult } from "@/lib/types";
import { formatPercent, jsonPreview } from "@/lib/format";
import { CandidateProducts } from "@/components/CandidateProducts";
import { MissingInfoPanel } from "@/components/MissingInfoPanel";
import { RetrievedKnowledge } from "@/components/RetrievedKnowledge";
import { AgentTraceTable } from "@/components/AgentTraceTable";
import { useI18n } from "@/lib/i18n";

export function AgentResultView({ result }: { result: AgentResult }) {
  const { t } = useI18n();

  return (
    <div className="space-y-5">
      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <h2 className="text-base font-semibold text-ink">{t("agent.title")}</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-4">
          <Summary label={t("agent.inquiryType")} value={result.inquiry_type} />
          <Summary label={t("agent.intent")} value={result.customer_intent} />
          <Summary label={t("agent.productCategory")} value={result.product_category} />
          <Summary label={t("agent.confidence")} value={formatPercent(result.confidence_score)} />
        </div>

        <div className="mt-5 grid gap-5 lg:grid-cols-2">
          <div>
            <h3 className="text-sm font-semibold text-slate-700">{t("agent.extractedRequirements")}</h3>
            <pre className="mt-2 rounded-md bg-panel p-3 text-xs leading-5 text-slate-700">
              {jsonPreview(result.extracted_requirements)}
            </pre>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-700">{t("agent.clarificationQuestions")}</h3>
            {result.clarification_questions.length ? (
              <ul className="mt-2 list-disc space-y-2 pl-5 text-sm text-slate-700">
                {result.clarification_questions.map((question) => (
                  <li key={question}>{question}</li>
                ))}
              </ul>
            ) : (
              <p className="mt-2 text-sm text-slate-500">{t("agent.noQuestions")}</p>
            )}
          </div>
        </div>

        <div className="mt-5">
          <h3 className="text-sm font-semibold text-slate-700">{t("agent.followUp")}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-700">{result.sales_follow_up_suggestion}</p>
        </div>
      </section>

      <MissingInfoPanel items={result.missing_information} />
      <CandidateProducts products={result.matched_products} />

      <section className="rounded-lg border border-red-200 bg-red-50 p-5 shadow-subtle">
        <h2 className="text-base font-semibold text-red-800">{t("agent.riskFlags")}</h2>
        {result.risk_flags.length ? (
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-red-700">
            {result.risk_flags.map((flag) => (
              <li key={flag}>{flag}</li>
            ))}
          </ul>
        ) : (
          <p className="mt-3 text-sm text-slate-500">{t("agent.noRiskFlags")}</p>
        )}
      </section>

      <RetrievedKnowledge items={result.retrieved_knowledge} />
      <AgentTraceTable steps={result.agent_trace} />

      <details className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <summary className="cursor-pointer text-sm font-semibold text-slate-700">{t("agent.jsonDebug")}</summary>
        <pre className="mt-4 rounded-md bg-panel p-3 text-xs leading-5 text-slate-700">
          {jsonPreview(result)}
        </pre>
      </details>
    </div>
  );
}

function Summary({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-panel p-3">
      <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</div>
      <div className="mt-2 text-sm font-semibold text-ink">{value || "-"}</div>
    </div>
  );
}
