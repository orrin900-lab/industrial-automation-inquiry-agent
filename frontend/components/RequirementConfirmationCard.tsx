"use client";

import type { AgentResult } from "@/lib/types";
import { formatPercent } from "@/lib/format";
import { useI18n } from "@/lib/i18n";

export function RequirementConfirmationCard({ result }: { result: AgentResult }) {
  const { language } = useI18n();
  const copy = language === "zh" ? zhCopy : enCopy;
  const specs = result.extracted_requirements.technical_specs || {};
  const specEntries = Object.entries(specs).filter(([, value]) => value);

  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
      <h2 className="text-base font-semibold text-ink">{copy.title}</h2>
      <div className="mt-4 grid gap-4 md:grid-cols-3">
        <Info label={copy.category} value={result.product_category || copy.pending} />
        <Info label={copy.confidence} value={formatPercent(result.confidence_score)} />
        <Info label={copy.intent} value={result.customer_intent || copy.pending} />
      </div>

      <div className="mt-5 grid gap-5 lg:grid-cols-2">
        <div>
          <h3 className="text-sm font-semibold text-slate-700">{copy.extracted}</h3>
          <dl className="mt-2 space-y-2 rounded-md bg-panel p-3 text-sm">
            <Spec label="brand" value={result.extracted_requirements.brand} pending={copy.pending} />
            <Spec label="model" value={result.extracted_requirements.model} pending={copy.pending} />
            <Spec label="quantity" value={result.extracted_requirements.quantity} pending={copy.pending} />
            <Spec label="application" value={result.extracted_requirements.application} pending={copy.pending} />
            {specEntries.map(([key, value]) => (
              <Spec key={key} label={key} value={String(value)} pending={copy.pending} />
            ))}
          </dl>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-slate-700">{copy.toConfirm}</h3>
          <ul className="mt-2 list-disc space-y-2 pl-5 text-sm text-slate-700">
            {(result.missing_information.length ? result.missing_information : [copy.noMissing]).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
          <h3 className="mt-4 text-sm font-semibold text-slate-700">{copy.questions}</h3>
          <ul className="mt-2 list-disc space-y-2 pl-5 text-sm text-slate-700">
            {(result.clarification_questions.length ? result.clarification_questions : [copy.noQuestions]).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="mt-4 rounded-md border border-amber-200 bg-amber-50 p-3 text-sm leading-6 text-amber-800">
        {copy.boundary}
      </div>
    </section>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-panel p-3">
      <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</div>
      <div className="mt-2 text-sm font-semibold text-ink">{value}</div>
    </div>
  );
}

function Spec({
  label,
  value,
  pending
}: {
  label: string;
  value?: string | null;
  pending: string;
}) {
  return (
    <div className="grid grid-cols-3 gap-3">
      <dt className="font-mono text-xs text-slate-500">{label}</dt>
      <dd className="col-span-2 text-slate-700">{value || pending}</dd>
    </div>
  );
}

const zhCopy = {
  title: "需求确认卡 Requirement Confirmation Card",
  category: "产品类别",
  confidence: "置信度",
  intent: "客户意图",
  extracted: "已抽取参数",
  toConfirm: "缺失 / 待确认信息",
  questions: "建议追问问题",
  pending: "待确认",
  noMissing: "暂无关键缺失信息",
  noQuestions: "暂无追问问题",
  boundary: "该卡片用于人工确认需求，不代表报价、库存或交期承诺。"
};

const enCopy = {
  title: "Requirement Confirmation Card",
  category: "Product Category",
  confidence: "Confidence",
  intent: "Customer Intent",
  extracted: "Extracted Parameters",
  toConfirm: "Missing / To Confirm",
  questions: "Questions to Ask",
  pending: "To confirm",
  noMissing: "No critical missing information",
  noQuestions: "No clarification questions",
  boundary: "This card supports manual requirement confirmation. It does not quote price, promise stock, or promise delivery time."
};
