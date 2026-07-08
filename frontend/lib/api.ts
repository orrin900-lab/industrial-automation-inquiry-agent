import type {
  AnalyzeResponse,
  InquiryDetail,
  InquiryInput,
  InquiryListItem,
  InquiryListParams,
  KnowledgeChunksResponse,
  KnowledgeStatus,
  KnowledgeReindexResponse,
  ReviewPayload,
  SampleInquiry
} from "@/lib/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";

export interface HealthResponse {
  status: string;
  service: string;
}

export interface InquiryListResponse {
  status: string;
  items: InquiryListItem[];
  limit: number;
  offset: number;
}

export interface SamplesResponse {
  status: string;
  samples: SampleInquiry[];
}

export interface ReviewResponse {
  status: string;
  inquiry_id: number;
  review_status: string;
}

function buildUrl(path: string, params?: Record<string, string | number | undefined>): string {
  const url = new URL(path, API_BASE_URL);

  Object.entries(params || {}).forEach(([key, value]) => {
    if (value !== undefined && value !== "") {
      url.searchParams.set(key, String(value));
    }
  });

  return url.toString();
}

async function requestJson<T>(
  path: string,
  options?: RequestInit,
  params?: Record<string, string | number | undefined>
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(buildUrl(path, params), {
      cache: "no-store",
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers || {})
      }
    });
  } catch {
    throw new Error(
      `Backend is not reachable. Please start FastAPI at ${API_BASE_URL}`
    );
  }

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const payload = await response.json();
      detail = payload.detail || JSON.stringify(payload);
    } catch {
      detail = await response.text();
    }
    throw new Error(detail || `API request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getHealth(): Promise<HealthResponse> {
  return requestJson<HealthResponse>("/api/health");
}

export function analyzeInquiry(payload: InquiryInput): Promise<AnalyzeResponse> {
  return requestJson<AnalyzeResponse>("/api/inquiries/analyze", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function getSampleInquiries(): Promise<SamplesResponse> {
  return requestJson<SamplesResponse>("/api/inquiries/samples");
}

export function getInquiries(params?: InquiryListParams): Promise<InquiryListResponse> {
  return requestJson<InquiryListResponse>("/api/inquiries", undefined, {
    status: params?.status,
    channel: params?.channel,
    product_category: params?.product_category,
    limit: params?.limit,
    offset: params?.offset
  });
}

export function getInquiryDetail(id: number | string): Promise<InquiryDetail> {
  return requestJson<InquiryDetail>(`/api/inquiries/${id}`);
}

export function submitReview(
  id: number | string,
  payload: ReviewPayload
): Promise<ReviewResponse> {
  return requestJson<ReviewResponse>(`/api/inquiries/${id}/review`, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function getKnowledgeStatus(): Promise<KnowledgeStatus> {
  return requestJson<KnowledgeStatus>("/api/knowledge/status");
}

export function getKnowledgeChunks(params?: {
  limit?: number;
  offset?: number;
  source_file?: string;
}): Promise<KnowledgeChunksResponse> {
  return requestJson<KnowledgeChunksResponse>("/api/knowledge/chunks", undefined, {
    limit: params?.limit,
    offset: params?.offset,
    source_file: params?.source_file
  });
}

export function rebuildKnowledgeIndex(): Promise<KnowledgeReindexResponse> {
  return requestJson<KnowledgeReindexResponse>("/api/knowledge/reindex", {
    method: "POST",
    body: JSON.stringify({})
  });
}
