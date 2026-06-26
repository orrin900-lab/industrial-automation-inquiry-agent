"use client";

import Link from "next/link";
import { useState } from "react";
import { analyzeInquiry } from "@/lib/api";
import type { AnalyzeResponse, InquiryInput } from "@/lib/types";
import { AgentResultView } from "@/components/AgentResultView";
import { InquiryForm } from "@/components/InquiryForm";

export default function AnalyzePage() {
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze(payload: InquiryInput) {
    setSubmitting(true);
    setError("");
    setResult(null);

    try {
      const response = await analyzeInquiry(payload);
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to analyze inquiry.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold text-ink">Analyze Inquiry</h1>
        <p className="mt-2 text-sm text-slate-600">
          Submit a website or email inquiry for structured qualification.
        </p>
      </section>

      <InquiryForm onSubmit={handleAnalyze} submitting={submitting} />

      {error ? (
        <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      ) : null}

      {result ? (
        <section className="space-y-5">
          <div className="rounded-lg border border-line bg-white p-5 shadow-subtle">
            <div className="grid gap-4 md:grid-cols-3">
              <div>
                <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">Inquiry ID</div>
                <div className="mt-1 text-lg font-semibold text-ink">#{result.inquiry_id}</div>
              </div>
              <div>
                <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">Agent Result ID</div>
                <div className="mt-1 text-lg font-semibold text-ink">#{result.agent_result_id}</div>
              </div>
              <div className="flex items-end">
                <Link
                  href={`/inquiries/${result.inquiry_id}`}
                  className="focus-ring rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white"
                >
                  View Detail
                </Link>
              </div>
            </div>
          </div>

          <AgentResultView result={result.agent_result} />
        </section>
      ) : null}
    </div>
  );
}
