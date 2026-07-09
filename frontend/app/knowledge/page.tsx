"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  getKnowledgeChunks,
  getKnowledgeStatus,
  rebuildKnowledgeIndex,
  uploadKnowledgeMarkdown
} from "@/lib/api";
import { AuthGuard } from "@/components/AuthGuard";
import type {
  KnowledgeChunkItem,
  KnowledgeChunksResponse,
  KnowledgeReindexResponse,
  KnowledgeStatus,
  KnowledgeUploadResponse
} from "@/lib/types";
import { formatDate } from "@/lib/format";
import { useI18n } from "@/lib/i18n";

const PAGE_SIZE = 10;

export default function KnowledgePage() {
  return (
    <AuthGuard allowedRoles={["admin"]}>
      <KnowledgePageContent />
    </AuthGuard>
  );
}

function KnowledgePageContent() {
  const { t } = useI18n();
  const [status, setStatus] = useState<KnowledgeStatus | null>(null);
  const [chunks, setChunks] = useState<KnowledgeChunksResponse | null>(null);
  const [sourceFile, setSourceFile] = useState("");
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true);
  const [rebuilding, setRebuilding] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [reindexResult, setReindexResult] = useState<KnowledgeReindexResponse | null>(null);
  const [uploadResult, setUploadResult] = useState<KnowledgeUploadResponse | null>(null);

  const loadStatus = useCallback(async () => {
    const response = await getKnowledgeStatus();
    setStatus(response);
    return response;
  }, []);

  const loadChunks = useCallback(async () => {
    const response = await getKnowledgeChunks({
      limit: PAGE_SIZE,
      offset,
      source_file: sourceFile
    });
    setChunks(response);
    return response;
  }, [offset, sourceFile]);

  const loadKnowledge = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      await Promise.all([loadStatus(), loadChunks()]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load knowledge base.");
    } finally {
      setLoading(false);
    }
  }, [loadChunks, loadStatus]);

  useEffect(() => {
    loadKnowledge();
  }, [loadKnowledge]);

  async function handleRebuild() {
    setRebuilding(true);
    setError("");
    setReindexResult(null);
    try {
      const result = await rebuildKnowledgeIndex();
      setReindexResult(result);
      await Promise.all([loadStatus(), loadChunks()]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to rebuild Qdrant index.");
    } finally {
      setRebuilding(false);
    }
  }

  async function handleUpload(file: File | null) {
    setError("");
    setUploadResult(null);
    if (!file) {
      return;
    }
    if (!file.name.toLowerCase().endsWith(".md")) {
      setError("Only Markdown .md files are allowed.");
      return;
    }
    if (file.size > 2 * 1024 * 1024) {
      setError("Markdown file is too large. Limit is 2MB.");
      return;
    }

    setUploading(true);
    try {
      const content = await file.text();
      const result = await uploadKnowledgeMarkdown({
        file_name: file.name,
        content
      });
      setUploadResult(result);
      await loadStatus();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to upload Markdown file.");
    } finally {
      setUploading(false);
    }
  }

  const sourceFiles = useMemo(() => {
    const fromStatus = status?.source_files || [];
    const fromChunks = chunks?.items.map((item) => item.source_file) || [];
    return Array.from(new Set([...fromStatus, ...fromChunks])).filter(Boolean);
  }, [chunks?.items, status?.source_files]);

  const canPrevious = offset > 0;
  const canNext = chunks ? offset + PAGE_SIZE < chunks.total : false;

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold text-ink">{t("knowledgeAdmin.title")}</h1>
        <p className="mt-2 max-w-4xl text-sm leading-6 text-slate-600">
          {t("knowledgeAdmin.description")}
        </p>
      </section>

      {error ? (
        <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      ) : null}

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-base font-semibold text-ink">{t("knowledgeAdmin.statusTitle")}</h2>
            {status?.error_message ? (
              <p className="mt-1 text-sm text-amber-700">{status.error_message}</p>
            ) : null}
          </div>
          <button
            type="button"
            onClick={loadKnowledge}
            className="focus-ring rounded-md border border-line bg-white px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
          >
            {t("knowledgeAdmin.refresh")}
          </button>
        </div>

        {loading && !status ? (
          <p className="text-sm text-slate-500">Loading...</p>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <StatusCard label={t("knowledgeAdmin.ragMode")} value={status?.rag_mode || "-"} />
            <StatusCard
              label={t("knowledgeAdmin.qdrantAvailable")}
              value={status?.qdrant_available ? t("common.yes") : t("common.no")}
              tone={status?.qdrant_available ? "green" : "amber"}
            />
            <StatusCard label={t("knowledgeAdmin.collection")} value={status?.collection_name || "-"} />
            <StatusCard label={t("knowledgeAdmin.pointsCount")} value={status?.points_count ?? 0} />
            <StatusCard label={t("knowledgeAdmin.vectorSize")} value={status?.vector_size ?? "-"} />
            <StatusCard label={t("knowledgeAdmin.embeddingProvider")} value={status?.embedding_provider || "-"} />
            <StatusCard
              label={t("knowledgeAdmin.fallback")}
              value={status?.fallback_available ? t("common.yes") : t("common.no")}
            />
            <StatusCard label={t("knowledgeAdmin.lastChecked")} value={formatDate(status?.last_checked_at)} />
          </div>
        )}

        <div className="mt-4 rounded-md border border-line bg-panel p-3 text-sm text-slate-600">
          <span className="font-semibold text-slate-700">{t("knowledgeAdmin.sourceFiles")}: </span>
          {sourceFiles.length ? sourceFiles.join(", ") : "-"}
        </div>
      </section>

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <h2 className="text-base font-semibold text-ink">{t("knowledgeAdmin.rebuildTitle")}</h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">
          {t("knowledgeAdmin.rebuildDescription")}
        </p>
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={handleRebuild}
            disabled={rebuilding}
            className="focus-ring rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
          >
            {rebuilding ? t("knowledgeAdmin.rebuilding") : t("knowledgeAdmin.rebuildButton")}
          </button>
          {reindexResult ? (
            <span className={reindexResult.success ? "text-sm text-emerald-700" : "text-sm text-red-700"}>
              {reindexResult.message}
              {reindexResult.points_count !== undefined && reindexResult.points_count !== null
                ? ` (${t("knowledgeAdmin.pointsCount")}: ${reindexResult.points_count})`
                : ""}
              {reindexResult.error_message ? ` ${reindexResult.error_message}` : ""}
            </span>
          ) : null}
        </div>
      </section>

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <h2 className="text-base font-semibold text-ink">Knowledge Upload</h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">
          Upload a Markdown .md file into the prototype knowledge upload directory. Rebuild the Qdrant index after upload to make the chunks retrievable.
        </p>
        <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center">
          <input
            type="file"
            accept=".md,text/markdown,text/plain"
            disabled={uploading}
            onChange={(event) => handleUpload(event.target.files?.[0] || null)}
            className="focus-ring rounded-md border border-line bg-white px-3 py-2 text-sm"
          />
          <span className="text-xs text-slate-500">
            .md only, max 2MB. Upload does not execute content and does not send email.
          </span>
        </div>
        {uploadResult ? (
          <div className={uploadResult.success ? "mt-3 rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-700" : "mt-3 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700"}>
            {uploadResult.message} ({uploadResult.file_name}, {uploadResult.size_bytes} bytes)
            {uploadResult.error_message ? ` ${uploadResult.error_message}` : ""}
          </div>
        ) : null}
      </section>

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h2 className="text-base font-semibold text-ink">{t("knowledgeAdmin.chunksTitle")}</h2>
            <p className="mt-1 text-sm text-slate-500">
              {t("knowledgeAdmin.total")}: {chunks?.total ?? 0}
            </p>
            {chunks?.error_message ? (
              <p className="mt-1 text-sm text-amber-700">{chunks.error_message}</p>
            ) : null}
          </div>
          <label className="w-full max-w-xs space-y-1">
            <span className="text-sm font-medium text-slate-700">{t("knowledgeAdmin.sourceFilter")}</span>
            <select
              value={sourceFile}
              onChange={(event) => {
                setOffset(0);
                setSourceFile(event.target.value);
              }}
              className="focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm"
            >
              <option value="">{t("knowledgeAdmin.allSources")}</option>
              {sourceFiles.map((file) => (
                <option key={file} value={file}>
                  {file}
                </option>
              ))}
            </select>
          </label>
        </div>

        <ChunkTable items={chunks?.items || []} />

        <div className="mt-4 flex items-center justify-between">
          <button
            type="button"
            disabled={!canPrevious}
            onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))}
            className="focus-ring rounded-md border border-line bg-white px-3 py-2 text-sm font-semibold text-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {t("knowledgeAdmin.previous")}
          </button>
          <span className="text-sm text-slate-500">
            {offset + 1}-{Math.min(offset + PAGE_SIZE, chunks?.total || 0)} / {chunks?.total || 0}
          </span>
          <button
            type="button"
            disabled={!canNext}
            onClick={() => setOffset(offset + PAGE_SIZE)}
            className="focus-ring rounded-md border border-line bg-white px-3 py-2 text-sm font-semibold text-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {t("knowledgeAdmin.next")}
          </button>
        </div>
      </section>

      <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <h2 className="text-base font-semibold text-ink">{t("knowledgeAdmin.notesTitle")}</h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">{t("knowledgeAdmin.notes")}</p>
      </section>
    </div>
  );
}

function StatusCard({
  label,
  value,
  tone = "default"
}: {
  label: string;
  value: string | number;
  tone?: "default" | "green" | "amber";
}) {
  const toneClass =
    tone === "green"
      ? "text-emerald-700"
      : tone === "amber"
      ? "text-amber-700"
      : "text-ink";

  return (
    <div className="rounded-md border border-line bg-panel p-3">
      <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</div>
      <div className={`mt-2 break-words text-sm font-semibold ${toneClass}`}>{value}</div>
    </div>
  );
}

function ChunkTable({ items }: { items: KnowledgeChunkItem[] }) {
  const { t } = useI18n();

  if (!items.length) {
    return (
      <div className="rounded-md border border-dashed border-line bg-panel p-4 text-sm text-slate-500">
        {t("knowledgeAdmin.noChunks")}
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-md border border-line">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-line text-sm">
          <thead className="bg-panel text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-3 py-2">{t("knowledgeAdmin.chunkId")}</th>
              <th className="px-3 py-2">{t("knowledgeAdmin.sourceFile")}</th>
              <th className="px-3 py-2">{t("knowledgeAdmin.sectionTitle")}</th>
              <th className="px-3 py-2">{t("knowledgeAdmin.documentType")}</th>
              <th className="px-3 py-2">{t("knowledgeAdmin.contentPreview")}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line bg-white">
            {items.map((item) => (
              <tr key={item.chunk_id}>
                <td className="max-w-[180px] px-3 py-3 font-mono text-xs text-slate-600">{item.chunk_id}</td>
                <td className="px-3 py-3 text-slate-700">{item.source_file}</td>
                <td className="px-3 py-3 text-slate-700">{item.section_title}</td>
                <td className="px-3 py-3 text-slate-700">{item.document_type}</td>
                <td className="min-w-[320px] px-3 py-3 leading-6 text-slate-600">{item.content_preview}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

