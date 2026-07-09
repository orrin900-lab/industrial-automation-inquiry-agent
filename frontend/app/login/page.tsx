"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/lib/api";
import { setAuthSession } from "@/lib/auth";
import { useI18n } from "@/lib/i18n";

const demoUsers = [
  { email: "admin@example.com", password: "admin123", role: "admin" },
  { email: "sales@example.com", password: "sales123", role: "sales" },
  { email: "support@example.com", password: "support123", role: "support" }
];

export default function LoginPage() {
  const router = useRouter();
  const { t } = useI18n();
  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("admin123");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await login({ email, password });
      setAuthSession(result.access_token, result.user);
      router.push("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : t("auth.loginFailed"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <section>
        <h1 className="text-2xl font-semibold text-ink">{t("auth.loginTitle")}</h1>
        <p className="mt-2 text-sm leading-6 text-slate-600">{t("auth.loginDescription")}</p>
      </section>

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">{t("auth.email")}</span>
            <input
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="focus-ring w-full rounded-md border border-line px-3 py-2 text-sm"
              required
            />
          </label>
          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">{t("auth.password")}</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="focus-ring w-full rounded-md border border-line px-3 py-2 text-sm"
              required
            />
          </label>

          {error ? <div className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div> : null}

          <button
            type="submit"
            disabled={loading}
            className="focus-ring rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? t("auth.loggingIn") : t("auth.loginButton")}
          </button>
        </form>
      </section>

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <h2 className="text-base font-semibold text-ink">{t("auth.demoUsers")}</h2>
        <div className="mt-3 grid gap-3 md:grid-cols-3">
          {demoUsers.map((user) => (
            <button
              type="button"
              key={user.email}
              onClick={() => {
                setEmail(user.email);
                setPassword(user.password);
              }}
              className="focus-ring rounded-md border border-line bg-panel p-3 text-left text-sm hover:bg-slate-50"
            >
              <div className="font-semibold text-ink">{user.role}</div>
              <div className="mt-1 text-slate-600">{user.email}</div>
              <div className="mt-1 font-mono text-xs text-slate-500">{user.password}</div>
            </button>
          ))}
        </div>
        <p className="mt-4 text-sm leading-6 text-slate-600">{t("auth.demoBoundary")}</p>
      </section>
    </div>
  );
}

