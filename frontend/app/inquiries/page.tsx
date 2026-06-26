"use client";

import { useEffect, useState } from "react";
import { getInquiries } from "@/lib/api";
import type { InquiryListItem } from "@/lib/types";
import { InquiryListTable } from "@/components/InquiryListTable";

export default function InquiriesPage() {
  const [items, setItems] = useState<InquiryListItem[]>([]);
  const [status, setStatus] = useState("");
  const [channel, setChannel] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    async function load() {
      setLoading(true);
      setError("");
      try {
        const response = await getInquiries({
          status,
          channel,
          limit: 100
        });
        if (mounted) {
          setItems(response.items || []);
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : "Failed to load inquiries.");
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    load();
    return () => {
      mounted = false;
    };
  }, [status, channel]);

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold text-ink">Inquiry List</h1>
        <p className="mt-2 text-sm text-slate-600">Review analyzed inquiries and open each record for follow-up.</p>
      </section>

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <div className="grid gap-4 md:grid-cols-3">
          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">Status</span>
            <select
              value={status}
              onChange={(event) => setStatus(event.target.value)}
              className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
            >
              <option value="">All statuses</option>
              <option value="pending_analysis">pending_analysis</option>
              <option value="analyzed">analyzed</option>
              <option value="pending_review">pending_review</option>
              <option value="need_clarification">need_clarification</option>
              <option value="ready_for_quotation">ready_for_quotation</option>
              <option value="invalid_lead">invalid_lead</option>
              <option value="completed">completed</option>
            </select>
          </label>

          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">Channel</span>
            <select
              value={channel}
              onChange={(event) => setChannel(event.target.value)}
              className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
            >
              <option value="">All channels</option>
              <option value="website">website</option>
              <option value="email">email</option>
            </select>
          </label>

          <div className="flex items-end text-sm text-slate-500">
            {loading ? "Loading..." : `${items.length} inquiries`}
          </div>
        </div>
      </section>

      {error ? (
        <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      ) : null}

      <InquiryListTable items={items} />
    </div>
  );
}
