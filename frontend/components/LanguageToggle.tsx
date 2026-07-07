"use client";

import { useI18n } from "@/lib/i18n";

export function LanguageToggle() {
  const { language, setLanguage, t } = useI18n();

  return (
    <div className="flex rounded-md border border-line bg-white p-1 text-sm" aria-label="Language switcher">
      <button
        type="button"
        onClick={() => setLanguage("zh")}
        className={`focus-ring rounded px-3 py-1 font-medium ${
          language === "zh" ? "bg-accent text-white" : "text-slate-600 hover:bg-slate-50"
        }`}
      >
        {t("language.zh")}
      </button>
      <button
        type="button"
        onClick={() => setLanguage("en")}
        className={`focus-ring rounded px-3 py-1 font-medium ${
          language === "en" ? "bg-accent text-white" : "text-slate-600 hover:bg-slate-50"
        }`}
      >
        {t("language.en")}
      </button>
    </div>
  );
}
