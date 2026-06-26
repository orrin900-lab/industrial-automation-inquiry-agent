import type { AgentTraceStep } from "@/lib/types";

export function AgentTraceTable({ steps }: { steps: AgentTraceStep[] }) {
  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-subtle">
      <h2 className="text-base font-semibold text-ink">Agent Execution Trace</h2>
      {!steps.length ? (
        <p className="mt-3 text-sm text-slate-500">No trace steps returned.</p>
      ) : (
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full divide-y divide-line text-sm">
            <thead className="bg-panel text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-3 py-2">Step</th>
                <th className="px-3 py-2">Mode</th>
                <th className="px-3 py-2">Success</th>
                <th className="px-3 py-2">Latency</th>
                <th className="px-3 py-2">Output Summary</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {steps.map((step, index) => (
                <tr key={`${step.step_name}-${index}`}>
                  <td className="px-3 py-2 font-medium text-ink">{step.step_name}</td>
                  <td className="px-3 py-2">
                    <span className="rounded-md bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-700">
                      {step.mode}
                    </span>
                  </td>
                  <td className="px-3 py-2">{step.success ? "Yes" : "No"}</td>
                  <td className="px-3 py-2">{Math.round(step.latency_ms)} ms</td>
                  <td className="max-w-xl px-3 py-2 text-slate-600">{step.output_summary}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
