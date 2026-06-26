export type InquiryChannel = "website" | "email" | string;

export interface InquiryInput {
  channel: InquiryChannel;
  customer_name?: string;
  customer_email?: string;
  company?: string;
  country?: string;
  subject?: string;
  message: string;
  attachments?: string[];
}

export interface ExtractedRequirement {
  brand?: string | null;
  model?: string | null;
  quantity?: string | null;
  product_category?: string | null;
  technical_specs?: Record<string, string>;
  application?: string | null;
  destination_country?: string | null;
  customer_company?: string | null;
  customer_contact?: string | null;
}

export interface Product {
  product_id: string;
  product_name: string;
  category: string;
  brand?: string | null;
  series?: string | null;
  model?: string | null;
  [key: string]: string | null | undefined;
}

export interface ProductCandidate {
  product_id: string;
  product_name: string;
  category: string;
  match_score: number;
  match_reason: string;
  missing_confirmations: string[];
  product?: Product | null;
}

export interface RetrievedKnowledge {
  content: string;
  score: number;
  metadata?: {
    source_file?: string;
    section_title?: string;
    chunk_id?: string | number;
    document_type?: string;
    [key: string]: unknown;
  };
}

export interface AgentTraceStep {
  step_name: string;
  mode: "rule" | "llm" | "fallback" | "mock" | "retrieval" | "hybrid" | string;
  input_summary: string;
  output_summary: string;
  success: boolean;
  error_message?: string | null;
  latency_ms: number;
}

export interface AgentResult {
  inquiry_type: string;
  customer_intent: string;
  product_category: string;
  extracted_requirements: ExtractedRequirement;
  missing_information: string[];
  matched_products: ProductCandidate[];
  clarification_questions: string[];
  english_reply_draft: string;
  risk_flags: string[];
  sales_follow_up_suggestion: string;
  confidence_score: number;
  agent_trace: AgentTraceStep[];
  retrieved_knowledge: RetrievedKnowledge[];
}

export interface AnalyzeResponse {
  status: string;
  inquiry_id: number;
  agent_result_id: number;
  agent_result: AgentResult;
}

export interface InquiryListItem {
  id: number;
  channel: string;
  customer_name?: string | null;
  company?: string | null;
  country?: string | null;
  subject?: string | null;
  status: string;
  product_category?: string | null;
  confidence_score?: number | null;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface InquiryRecord extends InquiryInput {
  id: number;
  status: string;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface ReviewLog {
  id: number;
  inquiry_id: number;
  reviewer_name: string;
  review_status: string;
  edited_reply?: string | null;
  reviewer_note?: string | null;
  created_at?: string | null;
}

export interface InquiryDetail {
  inquiry: InquiryRecord;
  agent_result?: (AgentResult & { id?: number; inquiry_id?: number; created_at?: string | null }) | null;
  review_logs: ReviewLog[];
}

export interface ReviewPayload {
  reviewer_name: string;
  review_status: string;
  edited_reply?: string;
  reviewer_note?: string;
}

export interface SampleInquiry {
  id?: string;
  channel?: string;
  customer_name?: string;
  customer_email?: string;
  company?: string;
  country?: string;
  subject?: string;
  message: string;
  expected_category?: string;
  [key: string]: unknown;
}

export interface InquiryListParams {
  status?: string;
  channel?: string;
  product_category?: string;
  limit?: number;
  offset?: number;
}
