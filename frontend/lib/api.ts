import type {
  AnalyzeResponse,
  AuthUser,
  InquiryDetail,
  InquiryInput,
  InquiryListItem,
  InquiryListParams,
  KnowledgeChunksResponse,
  KnowledgeStatus,
  KnowledgeReindexResponse,
  KnowledgeUploadInput,
  KnowledgeUploadResponse,
  LoginPayload,
  LoginResponse,
  ProductLibraryInput,
  ProductLibraryResponse,
  PublicInquiryInput,
  PublicInquiryResponse,
  ReviewPayload,
  SampleInquiry,
  SystemStatus
} from "@/lib/types";
import { authHeader } from "@/lib/auth";

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
        ...authHeader(),
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

export function getSystemStatus(): Promise<SystemStatus> {
  return requestJson<SystemStatus>("/api/system/status");
}

export function login(payload: LoginPayload): Promise<LoginResponse> {
  return requestJson<LoginResponse>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function getCurrentUser(): Promise<AuthUser> {
  return requestJson<AuthUser>("/api/auth/me");
}

export function logout(): Promise<{ status: string; message: string }> {
  return requestJson<{ status: string; message: string }>("/api/auth/logout", {
    method: "POST",
    body: JSON.stringify({})
  });
}

export function analyzeInquiry(payload: InquiryInput): Promise<AnalyzeResponse> {
  return requestJson<AnalyzeResponse>("/api/inquiries/analyze", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function submitPublicInquiry(
  payload: PublicInquiryInput
): Promise<PublicInquiryResponse> {
  return requestJson<PublicInquiryResponse>("/api/public/inquiries", {
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

export function updateInquiryStatus(
  id: number | string,
  status: string
): Promise<{ status: string; inquiry: unknown }> {
  return requestJson<{ status: string; inquiry: unknown }>(`/api/inquiries/${id}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status })
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

export function uploadKnowledgeMarkdown(
  payload: KnowledgeUploadInput
): Promise<KnowledgeUploadResponse> {
  return requestJson<KnowledgeUploadResponse>("/api/knowledge/upload", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function getProducts(params?: {
  category?: string;
  query?: string;
  active_only?: boolean;
  limit?: number;
  offset?: number;
}): Promise<ProductLibraryResponse> {
  return requestJson<ProductLibraryResponse>("/api/products", undefined, {
    category: params?.category,
    query: params?.query,
    active_only: params?.active_only ? "true" : undefined,
    limit: params?.limit,
    offset: params?.offset
  });
}

export function createProduct(
  payload: ProductLibraryInput
): Promise<{ status: string; product: unknown }> {
  return requestJson<{ status: string; product: unknown }>("/api/products", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function updateProductStatus(
  productId: string,
  isActive: boolean
): Promise<{ status: string; product: unknown }> {
  return requestJson<{ status: string; product: unknown }>(`/api/products/${productId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ is_active: isActive })
  });
}
