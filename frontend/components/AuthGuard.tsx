"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getCurrentUser } from "@/lib/api";
import { clearAuthSession, getStoredUser } from "@/lib/auth";
import type { AuthUser } from "@/lib/types";
import { useI18n } from "@/lib/i18n";

export function AuthGuard({
  allowedRoles,
  children
}: {
  allowedRoles?: string[];
  children: React.ReactNode;
}) {
  const { t } = useI18n();
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    setUser(getStoredUser());
    getCurrentUser()
      .then((currentUser) => {
        if (active) {
          setUser(currentUser);
          setError("");
        }
      })
      .catch((err) => {
        if (active) {
          clearAuthSession();
          setUser(null);
          setError(err instanceof Error ? err.message : t("auth.loginRequired"));
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [t]);

  if (loading) {
    return <div className="rounded-lg border border-line bg-white p-6 text-sm text-slate-500">{t("auth.checking")}</div>;
  }

  if (!user) {
    return (
      <div className="rounded-lg border border-amber-200 bg-amber-50 p-6 text-sm text-amber-800">
        <p>{t("auth.loginRequired")}</p>
        <Link href="/login" className="mt-3 inline-flex rounded-md bg-accent px-3 py-2 text-sm font-semibold text-white">
          {t("auth.goLogin")}
        </Link>
      </div>
    );
  }

  if (allowedRoles?.length && !allowedRoles.includes(user.role)) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-sm text-red-700">
        <p className="font-semibold">{t("auth.noPermission")}</p>
        <p className="mt-2">{t("auth.adminOnly")}</p>
      </div>
    );
  }

  if (error) {
    return <div className="rounded-lg border border-amber-200 bg-amber-50 p-6 text-sm text-amber-800">{error}</div>;
  }

  return <>{children}</>;
}
