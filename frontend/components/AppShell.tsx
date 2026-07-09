"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LanguageToggle } from "@/components/LanguageToggle";
import { UserMenu } from "@/components/UserMenu";
import { getStoredUser } from "@/lib/auth";
import { useI18n } from "@/lib/i18n";
import { useEffect, useState } from "react";
import type { AuthUser } from "@/lib/types";

const navItems = [
  { href: "/public-inquiry", labelKey: "nav.publicInquiry", public: true, adminOnly: false },
  { href: "/", labelKey: "nav.dashboard", public: false, adminOnly: false },
  { href: "/analyze", labelKey: "nav.analyze", public: false, adminOnly: false },
  { href: "/inquiries", labelKey: "nav.inquiries", public: false, adminOnly: false },
  { href: "/products", labelKey: "nav.products", public: false, adminOnly: true },
  { href: "/knowledge", labelKey: "nav.knowledge", public: false, adminOnly: true }
] as const;

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
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

  const visibleNavItems = navItems.filter(
    (item) =>
      item.public || (!item.adminOnly && user) || (item.adminOnly && user?.role === "admin")
  );

  return (
    <div className="min-h-screen bg-[#eef2f7]">
      <header className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
          <Link href="/" className="focus-ring rounded-sm">
            <div className="text-lg font-semibold text-ink">Industrial Automation Inquiry Agent</div>
            <div className="text-sm text-slate-500">{t("app.subtitle")}</div>
          </Link>

          <div className="flex flex-wrap items-center gap-3">
            <nav className="flex flex-wrap gap-2">
              {visibleNavItems.map((item) => {
                const active =
                  item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`focus-ring rounded-md px-3 py-2 text-sm font-medium ${
                      active
                        ? "bg-accent text-white"
                        : "border border-line bg-white text-slate-700 hover:bg-slate-50"
                    }`}
                  >
                    {t(item.labelKey)}
                  </Link>
                );
              })}
            </nav>
            <UserMenu />
            <LanguageToggle />
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{children}</main>
    </div>
  );
}
