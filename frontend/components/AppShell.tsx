"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "Dashboard" },
  { href: "/analyze", label: "Analyze Inquiry" },
  { href: "/inquiries", label: "Inquiry List" }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-[#eef2f7]">
      <header className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
          <Link href="/" className="focus-ring rounded-sm">
            <div className="text-lg font-semibold text-ink">Industrial Automation Inquiry Agent</div>
            <div className="text-sm text-slate-500">Sales operations console</div>
          </Link>

          <nav className="flex flex-wrap gap-2">
            {navItems.map((item) => {
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
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{children}</main>
    </div>
  );
}
