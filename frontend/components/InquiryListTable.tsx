import Link from "next/link";
import type { InquiryListItem } from "@/lib/types";
import { formatDate, formatPercent, statusLabel } from "@/lib/format";

export function InquiryListTable({ items }: { items: InquiryListItem[] }) {
  if (!items.length) {
    return (
      <div className="rounded-lg border border-line bg-white p-6 text-sm text-slate-500">
        No inquiries found.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg border border-line bg-white shadow-subtle">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-line text-sm">
          <thead className="bg-panel text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-3">ID</th>
              <th className="px-4 py-3">Channel</th>
              <th className="px-4 py-3">Customer</th>
              <th className="px-4 py-3">Company</th>
              <th className="px-4 py-3">Country</th>
              <th className="px-4 py-3">Subject</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Category</th>
              <th className="px-4 py-3">Confidence</th>
              <th className="px-4 py-3">Created</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {items.map((item) => (
              <tr key={item.id} className="hover:bg-slate-50">
                <td className="px-4 py-3 font-medium text-accent">
                  <Link href={`/inquiries/${item.id}`} className="focus-ring rounded-sm">
                    #{item.id}
                  </Link>
                </td>
                <td className="px-4 py-3">{item.channel}</td>
                <td className="px-4 py-3">{item.customer_name || "-"}</td>
                <td className="px-4 py-3">{item.company || "-"}</td>
                <td className="px-4 py-3">{item.country || "-"}</td>
                <td className="max-w-[260px] px-4 py-3">
                  <Link href={`/inquiries/${item.id}`} className="focus-ring rounded-sm text-slate-800 hover:text-accent">
                    {item.subject || "Untitled inquiry"}
                  </Link>
                </td>
                <td className="px-4 py-3">{statusLabel(item.status)}</td>
                <td className="px-4 py-3">{item.product_category || "-"}</td>
                <td className="px-4 py-3">{formatPercent(item.confidence_score)}</td>
                <td className="px-4 py-3 text-slate-500">{formatDate(item.created_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
