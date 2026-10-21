import type { ApplicationPayload, CreditApplication } from "./types";

const API_URL = import.meta.env.VITE_API_URL ?? "/api/v1";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail = body?.detail;
    const message = typeof detail === "string" ? detail : "Не удалось выполнить запрос";
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

export const createApplication = (payload: ApplicationPayload) =>
  request<CreditApplication>("/applications", {
    method: "POST",
    body: JSON.stringify(payload),
  });

export const submitApplication = (id: string) =>
  request<CreditApplication>(`/applications/${id}/submit`, { method: "POST" });

export const acceptOffer = (id: string) =>
  request<CreditApplication>(`/applications/${id}/accept`, { method: "POST" });

