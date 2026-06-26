"use client";

import { FormEvent, useState } from "react";
import { submitReview } from "@/lib/api";

const reviewStatuses = [
  "pending_review",
  "need_clarification",
  "ready_for_quotation",
  "invalid_lead",
  "completed"
];

export function ReviewForm({
  inquiryId,
  editedReply,
  onSubmitted
}: {
  inquiryId: number;
  editedReply: string;
  onSubmitted?: () => void;
}) {
  const [reviewerName, setReviewerName] = useState("Sales User");
  const [reviewStatus, setReviewStatus] = useState("need_clarification");
  const [reviewerNote, setReviewerNote] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    setMessage("");

    try {
      await submitReview(inquiryId, {
        reviewer_name: reviewerName,
        review_status: reviewStatus,
        edited_reply: editedReply,
        reviewer_note: reviewerNote
      });
      setMessage(`Review saved as ${reviewStatus}.`);
      onSubmitted?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit review.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
      <h2 className="text-base font-semibold text-ink">Review Form</h2>
      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <div className="grid gap-4 md:grid-cols-2">
          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">Reviewer Name</span>
            <input
              value={reviewerName}
              onChange={(event) => setReviewerName(event.target.value)}
              className="focus-ring w-full rounded-md border border-line px-3 py-2 text-sm"
              required
            />
          </label>

          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">Review Status</span>
            <select
              value={reviewStatus}
              onChange={(event) => setReviewStatus(event.target.value)}
              className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
            >
              {reviewStatuses.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </label>
        </div>

        <label className="space-y-1">
          <span className="text-sm font-medium text-slate-700">Reviewer Note</span>
          <textarea
            value={reviewerNote}
            onChange={(event) => setReviewerNote(event.target.value)}
            rows={4}
            className="focus-ring w-full rounded-md border border-line px-3 py-2 text-sm leading-6"
          />
        </label>

        {message ? <div className="rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-700">{message}</div> : null}
        {error ? <div className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div> : null}

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={submitting}
            className="focus-ring rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
          >
            {submitting ? "Saving..." : "Submit Review"}
          </button>
        </div>
      </form>
    </section>
  );
}
