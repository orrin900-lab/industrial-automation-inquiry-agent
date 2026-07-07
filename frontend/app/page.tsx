"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { getHealth, getInquiries } from "@/lib/api";
import type { HealthResponse, InquiryListResponse } from "@/lib/api";
import { InquiryListTable } from "@/components/InquiryListTable";
import { StatCard } from "@/components/StatCard";
import { useI18n } from "@/lib/i18n";

export default function DashboardPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthError, setHealthError] = useState("");
  const [inquiries, setInquiries] = useState<InquiryListResponse | null>(null);
  const [inquiryError, setInquiryError] = useState("");
  const [loading, setLoading] = useState(true);
  const { t } = useI18n();

  useEffect(() => {
    let mounted = true;

    async function load() {
      setLoading(true);
      try {
        const [healthPayload, inquiryPayload] = await Promise.all([
          getHealth(),
          getInquiries({ limit: 50 })
        ]);

        if (mounted) {
          setHealth(healthPayload);
          setInquiries(inquiryPayload);
        }
      } catch (error) {
        if (mounted) {
          const message = error instanceof Error ? error.message : "Failed to load dashboard.";
          setHealthError(message);
          setInquiryError(message);
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
  }, []);

  const items = inquiries?.items || [];
  const stats = useMemo(() => {
    const pending = items.filter((item) => item.status === "pending_review").length;
    const analyzed = items.filter((item) => item.status === "analyzed" || item.status === "pending_review").length;
    return {
      total: items.length,
      pending,
      analyzed,
      recent: items.slice(0, 5)
    };
  }, [items]);

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-line bg-white p-6 shadow-subtle">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-ink">{t("dashboard.title")}</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
              {t("dashboard.description")}
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              <Link href="/analyze" className="focus-ring rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white">
                {t("dashboard.ctaAnalyze")}
              </Link>
              <Link href="/inquiries" className="focus-ring rounded-md border border-line bg-white px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50">
                {t("dashboard.ctaList")}
              </Link>
            </div>
          </div>

          <div className="rounded-md border border-line bg-panel px-4 py-3 text-sm">
            <div className="font-semibold text-slate-700">{t("dashboard.backendStatus")}</div>
            {health ? (
              <div className="mt-1 text-emerald-700">{health.status} · {health.service}</div>
            ) : (
              <div className="mt-1 text-slate-500">{loading ? t("dashboard.checking") : t("dashboard.unavailable")}</div>
            )}
          </div>
        </div>
      </section>

      {healthError ? <Alert message={healthError} /> : null}

      <div className="grid gap-4 md:grid-cols-4">
        <StatCard label={t("dashboard.total")} value={stats.total} caption={t("dashboard.totalCaption")} />
        <StatCard label={t("dashboard.pending")} value={stats.pending} caption={t("dashboard.pendingCaption")} />
        <StatCard label={t("dashboard.analyzed")} value={stats.analyzed} caption={t("dashboard.analyzedCaption")} />
        <StatCard label={t("dashboard.recent")} value={stats.recent.length} caption={t("dashboard.recentCaption")} />
      </div>

      {inquiryError && !healthError ? <Alert message={inquiryError} /> : null}

      <section>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-ink">{t("dashboard.recent")}</h2>
          <Link href="/inquiries" className="focus-ring rounded-sm text-sm font-semibold text-accent">
            {t("dashboard.viewAll")}
          </Link>
        </div>
        <InquiryListTable items={stats.recent} />
      </section>
    </div>
  );
}

function Alert({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
      {message}
    </div>
  );
}
