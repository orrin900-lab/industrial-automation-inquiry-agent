"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getInquiryDetail } from "@/lib/api";
import type { InquiryDetail } from "@/lib/types";
import { AgentResultView } from "@/components/AgentResultView";
import { ReplyDraftEditor } from "@/components/ReplyDraftEditor";
import { ReviewForm } from "@/components/ReviewForm";
import { formatDate } from "@/lib/format";
import { useI18n } from "@/lib/i18n";

export default function InquiryDetailPage() {
  const params = useParams<{ id: string }>();
  const inquiryId = params.id;
  const [detail, setDetail] = useState<InquiryDetail | null>(null);
  const [replyDraft, setReplyDraft] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { t, statusText } = useI18n();

  const loadDetail = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const response = await getInquiryDetail(inquiryId);
      setDetail(response);
      setReplyDraft(response.agent_result?.english_reply_draft || "");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load inquiry detail.");
    } finally {
      setLoading(false);
    }
  }, [inquiryId]);

  useEffect(() => {
    loadDetail();
  }, [loadDetail]);

  if (loading) {
    return <div className="rounded-lg border border-line bg-white p-6 text-sm text-slate-500">{t("detail.loading")}</div>;
  }

  if (error) {
    return <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>;
  }

  if (!detail) {
    return <div className="rounded-lg border border-line bg-white p-6 text-sm text-slate-500">{t("detail.notFound")}</div>;
  }

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold text-ink">{t("detail.titlePrefix")} #{detail.inquiry.id}</h1>
        <p className="mt-2 text-sm text-slate-600">{detail.inquiry.subject || t("table.untitled")}</p>
      </section>

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <h2 className="text-base font-semibold text-ink">{t("detail.originalInquiry")}</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Info label={t("detail.channel")} value={detail.inquiry.channel} />
          <Info label={t("detail.status")} value={statusText(detail.inquiry.status)} />
          <Info label={t("detail.customer")} value={detail.inquiry.customer_name || "-"} />
          <Info label={t("detail.email")} value={detail.inquiry.customer_email || "-"} />
          <Info label={t("detail.company")} value={detail.inquiry.company || "-"} />
          <Info label={t("detail.country")} value={detail.inquiry.country || "-"} />
          <Info label={t("detail.created")} value={formatDate(detail.inquiry.created_at)} />
          <Info label={t("detail.updated")} value={formatDate(detail.inquiry.updated_at)} />
        </div>
        <div className="mt-5">
          <h3 className="text-sm font-semibold text-slate-700">{t("detail.message")}</h3>
          <p className="mt-2 rounded-md bg-panel p-3 text-sm leading-6 text-slate-700">{detail.inquiry.message}</p>
        </div>
      </section>

      {detail.agent_result ? (
        <>
          <AgentResultView result={detail.agent_result} />
          <ReplyDraftEditor value={replyDraft} onChange={setReplyDraft} />
          <ReviewForm
            inquiryId={detail.inquiry.id}
            editedReply={replyDraft}
            onSubmitted={loadDetail}
          />
        </>
      ) : (
        <div className="rounded-lg border border-line bg-white p-6 text-sm text-slate-500">
          {t("detail.noAgentResult")}
        </div>
      )}

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <h2 className="text-base font-semibold text-ink">{t("detail.reviewLogs")}</h2>
        {!detail.review_logs.length ? (
          <p className="mt-3 text-sm text-slate-500">{t("detail.noReviewLogs")}</p>
        ) : (
          <div className="mt-4 space-y-3">
            {detail.review_logs.map((log) => (
              <article key={log.id} className="rounded-md border border-line bg-panel p-4 text-sm">
                <div className="font-semibold text-ink">
                  {log.reviewer_name} · {statusText(log.review_status)}
                </div>
                <div className="mt-1 text-slate-500">{formatDate(log.created_at)}</div>
                {log.reviewer_note ? <p className="mt-3 leading-6 text-slate-700">{log.reviewer_note}</p> : null}
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-panel p-3">
      <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</div>
      <div className="mt-2 text-sm font-medium text-ink">{value}</div>
    </div>
  );
}
