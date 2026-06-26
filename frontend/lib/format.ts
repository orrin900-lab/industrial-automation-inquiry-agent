export function formatDate(value?: string | null): string {
  if (!value) {
    return "-";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat("en", {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit"
  }).format(date);
}

export function formatPercent(value?: number | null): string {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "-";
  }

  return `${Math.round(value * 100)}%`;
}

export function statusLabel(status?: string | null): string {
  if (!status) {
    return "-";
  }

  return status
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function truncate(value: string, length = 160): string {
  if (!value) {
    return "";
  }

  return value.length > length ? `${value.slice(0, length).trim()}...` : value;
}

export function jsonPreview(value: unknown): string {
  return JSON.stringify(value, null, 2);
}
