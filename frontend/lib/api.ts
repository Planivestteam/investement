const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function req(path: string, options: RequestInit = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    cache: "no-store",
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Erro ${res.status}`);
  }
  return res.json();
}

export const api = {
  dashboard: () => req("/api/dashboard"),
  asset: (ticker: string, period = "1y") => req(`/api/asset/${encodeURIComponent(ticker)}?period=${period}`),
  search: (q: string) => req(`/api/search?q=${encodeURIComponent(q)}`),
  news: (ticker: string) => req(`/api/news/${encodeURIComponent(ticker)}`),
  score: (ticker: string) => req(`/api/score/${encodeURIComponent(ticker)}`),
  analyze: (ticker: string) => req(`/api/ai/analyze/${encodeURIComponent(ticker)}`),
  chat: (mensagens: { role: string; content: string }[], perfil?: any) =>
    req(`/api/ai/chat`, { method: "POST", body: JSON.stringify({ mensagens, perfil }) }),
  comparar: (tickers: string[]) =>
    req(`/api/ai/comparar`, { method: "POST", body: JSON.stringify(tickers) }),
};
