"use client";
import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const [resultados, setResultados] = useState<any[]>([]);
  const [aberto, setAberto] = useState(false);
  const timer = useRef<any>(null);
  const router = useRouter();

  function onChange(v: string) {
    setQuery(v);
    if (timer.current) clearTimeout(timer.current);
    if (!v.trim()) {
      setResultados([]);
      return;
    }
    timer.current = setTimeout(async () => {
      try {
        const data = await api.search(v);
        setResultados(data.resultados || []);
        setAberto(true);
      } catch {
        setResultados([]);
      }
    }, 250);
  }

  function irPara(ticker: string) {
    setAberto(false);
    setQuery("");
    router.push(`/ativo/${encodeURIComponent(ticker)}`);
  }

  return (
    <div className="relative max-w-md mx-auto">
      <input
        value={query}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => resultados.length && setAberto(true)}
        onBlur={() => setTimeout(() => setAberto(false), 150)}
        placeholder="Pesquisar ações, ETFs, cripto..."
        className="w-full px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-sm outline-none focus:ring-2 focus:ring-blue-500"
      />
      {aberto && resultados.length > 0 && (
        <div className="absolute mt-1 w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg shadow-lg overflow-hidden z-50">
          {resultados.map((r) => (
            <button
              key={r.ticker}
              onMouseDown={() => irPara(r.ticker)}
              className="w-full text-left px-4 py-2 text-sm hover:bg-slate-100 dark:hover:bg-slate-800 flex justify-between"
            >
              <span>{r.nome}</span>
              <span className="text-slate-400">{r.ticker}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
