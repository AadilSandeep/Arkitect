/**
 * API client — typed methods for all backend endpoints.
 *
 * Automatically attaches the Supabase access token to every request.
 * Falls back to localhost:8000 when VITE_API_URL is not set.
 */

import { supabase } from "./supabase";

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

// ---------------------------------------------------------------------------
// Error class
// ---------------------------------------------------------------------------

export class ApiError extends Error {
  status: number;
  body: string;

  constructor(status: number, body: string) {
    super(`API Error ${status}: ${body}`);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

// ---------------------------------------------------------------------------
// Core fetch wrapper
// ---------------------------------------------------------------------------

async function apiClient<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  // Get current session token
  const {
    data: { session },
  } = await supabase.auth.getSession();
  const token = session?.access_token;

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const body = await res.text();
    throw new ApiError(res.status, body);
  }

  // 204 No Content — return undefined
  if (res.status === 204) {
    return undefined as T;
  }

  return res.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Types (matching backend response schemas)
// ---------------------------------------------------------------------------

export interface WorkflowSummary {
  id: string;
  goal: string;
  domain: string;
  complexity: string;
  estimated_time: string;
  created_at: string;
}

export interface PaginatedWorkflows {
  items: WorkflowSummary[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

export interface WorkflowDetail {
  id: string;
  goal: string;
  domain: string;
  complexity: string;
  estimated_time: string;
  response_data: WorkflowResponseData;
  created_at: string;
  updated_at: string;
}

/** Matches backend WorkflowResponse schema */
export interface WorkflowResponseData {
  goal: {
    user_input: string;
    domain: string;
    goal_type: string;
    complexity: string;
  };
  deliverables: Array<{
    id: number;
    title: string;
    description: string;
  }>;
  recommended_tools: Array<{
    name: string;
    category: string;
    reason: string;
  }>;
  workflow: Array<{
    step_number: number;
    title: string;
    tool: string;
    why: string;
    what_to_do: string;
    prompt: string;
    expected_result: string;
  }>;
  alternative_workflows: {
    fastest: { summary: string; tools: string[] };
    cheapest: { summary: string; tools: string[] };
    highest_quality: { summary: string; tools: string[] };
    beginner_friendly: { summary: string; tools: string[] };
  };
  knowledge_areas: {
    high: string[];
    medium: string[];
    low: string[];
  };
  estimated_time: string;
}

export interface SavedWorkflowResponse {
  id: string;
  workflow_data: WorkflowResponseData;
}

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  avatar_url: string;
  created_at: string;
  updated_at: string;
}

// ---------------------------------------------------------------------------
// API methods
// ---------------------------------------------------------------------------

export const api = {
  // ── Workflow Generation ──────────────────────────────────────────────
  generateWorkflow: (goal: string) =>
    apiClient<SavedWorkflowResponse>("/api/v1/workflow/generate", {
      method: "POST",
      body: JSON.stringify({ goal }),
    }),

  // ── Workflow CRUD ────────────────────────────────────────────────────
  listWorkflows: (page = 1, perPage = 20) =>
    apiClient<PaginatedWorkflows>(
      `/api/v1/workflows/?page=${page}&per_page=${perPage}`
    ),

  getWorkflow: (id: string) =>
    apiClient<WorkflowDetail>(`/api/v1/workflows/${id}`),

  deleteWorkflow: (id: string) =>
    apiClient<void>(`/api/v1/workflows/${id}`, { method: "DELETE" }),

  // ── Auth ─────────────────────────────────────────────────────────────
  getMe: () => apiClient<UserProfile>("/api/v1/auth/me"),

  // ── Health ───────────────────────────────────────────────────────────
  healthCheck: () => apiClient<{ status: string }>("/"),
};