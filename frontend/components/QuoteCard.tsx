"use client";
import Link from "next/link";

export default function QuoteCard({ q }: { q: any }) {
  if (!q) return null;
  const positivo = (q.variacao_pct ?? 0) >= 0;
  return (
    <Link
      href={`/ativo/${encodeURIComponent(q.ticker)}`}
      className="card hover:shadow-md transition-shadow flex flex-col gap-1 min-w-[150px]"
    >
      <span className="text-xs text-slate-500">{q.ticker}</span>
      <span className="text-lg font-semibold">
        {q.preco != null ? q.preco.toLocaleString("pt-PT", { maximumFractionDigits: 2 }) : "—"}
      </span>
      <span className={`text-sm font-medium ${positivo ? "text-subida" : "text-descida"}`}>
        {q.variacao_pct != null ? `${positivo ? "▲" : "▼"} ${Math.abs(q.variacao_pct).toFixed(2)}%` : "—"}
      </span>
    </Link>
  );
}
