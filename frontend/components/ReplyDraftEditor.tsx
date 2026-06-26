"use client";

export function ReplyDraftEditor({
  value,
  onChange
}: {
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
      <h2 className="text-base font-semibold text-ink">English Reply Draft</h2>
      <textarea
        value={value}
        onChange={(event) => onChange(event.target.value)}
        rows={9}
        className="focus-ring mt-4 w-full rounded-md border border-line bg-white px-3 py-2 text-sm leading-6"
      />
      <p className="mt-2 text-xs text-slate-500">
        This draft remains internal until a sales user reviews and sends it manually.
      </p>
    </section>
  );
}
