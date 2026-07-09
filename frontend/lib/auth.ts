import type { AuthUser } from "@/lib/types";

const TOKEN_KEY = "industrial-agent-auth-token";
const USER_KEY = "industrial-agent-auth-user";

export function getAuthToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setAuthSession(token: string, user: AuthUser) {
  window.localStorage.setItem(TOKEN_KEY, token);
  window.localStorage.setItem(USER_KEY, JSON.stringify(user));
  window.dispatchEvent(new Event("auth-session-changed"));
}

export function clearAuthSession() {
  window.localStorage.removeItem(TOKEN_KEY);
  window.localStorage.removeItem(USER_KEY);
  window.dispatchEvent(new Event("auth-session-changed"));
}

export function getStoredUser(): AuthUser | null {
  if (typeof window === "undefined") {
    return null;
  }
  const raw = window.localStorage.getItem(USER_KEY);
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw) as AuthUser;
  } catch {
    clearAuthSession();
    return null;
  }
}

export function authHeader(): Record<string, string> {
  const token = getAuthToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

