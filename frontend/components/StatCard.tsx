export function StatCard({
  label,
  value,
  caption
}: {
  label: string;
  value: string | number;
  caption?: string;
}) {
  return (
    <section className="rounded-lg border border-line bg-white p-4 shadow-subtle">
      <div className="text-sm font-medium text-slate-500">{label}</div>
      <div className="mt-2 text-3xl font-semibold text-ink">{value}</div>
      {caption ? <div className="mt-2 text-sm text-slate-500">{caption}</div> : null}
    </section>
  );
}
