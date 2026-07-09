"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { clearAuthSession, getStoredUser } from "@/lib/auth";
import type { AuthUser } from "@/lib/types";
import { useI18n } from "@/lib/i18n";

export function UserMenu() {
  const { t } = useI18n();
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    function syncUser() {
      setUser(getStoredUser());
    }

    syncUser();
    window.addEventListener("auth-session-changed", syncUser);
    window.addEventListener("storage", syncUser);
    return () => {
      window.removeEventListener("auth-session-changed", syncUser);
      window.removeEventListener("storage", syncUser);
    };
  }, []);

  if (!user) {
    return (
      <Link
        href="/login"
        className="focus-ring rounded-md border border-line bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
      >
        {t("nav.login")}
      </Link>
    );
  }

  return (
    <div className="flex items-center gap-2 rounded-md border border-line bg-panel px-3 py-2 text-sm text-slate-700">
      <span className="font-medium text-ink">{user.name}</span>
      <span className="rounded bg-white px-2 py-0.5 text-xs font-semibold uppercase text-slate-600">{user.role}</span>
      <button
        type="button"
        onClick={clearAuthSession}
        className="focus-ring rounded px-2 py-1 text-xs font-semibold text-accent hover:bg-white"
      >
        {t("auth.logout")}
      </button>
    </div>
  );
}

