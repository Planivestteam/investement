"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import QuoteCard from "@/components/QuoteCard";

export default function DashboardPage() {
  const [dados, setDados] = useState<any>(null);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    api.dashboard().then(setDados).catch((e) => setErro(e.message));
  }, []);

  if (erro) return <div className="text-red-600">Erro ao carregar dashboard: {erro}</div>;
  if (!dados) return <div className="text-slate-500">A carregar dados de mercado...</div>;

  return (
    <div className="space-y-8">
      {dados.resumo_ia && (
        <div className="card bg-blue-50 dark:bg-blue-950/30 border-blue-200 dark:border-blue-900">
          <h2 className="font-semibold mb-2">🤖 Resumo diário da IA</h2>
          <p className="text-sm leading-relaxed">{dados.resumo_ia}</p>
        </div>
      )}

      <Secao titulo="Índices Mundiais" itens={dados.indices} />
      <Secao titulo="Criptomoedas" itens={dados.criptomoedas} />
      <Secao titulo="Ações em Destaque" itens={dados.acoes_destaque} />
      <Secao titulo="Commodities" itens={dados.commodities} />
      <Secao titulo="Forex" itens={dados.forex} />

      <div className="grid md:grid-cols-2 gap-6">
        <Secao titulo="📈 Maiores Subidas" itens={dados.maiores_subidas} />
        <Secao titulo="📉 Maiores Quedas" itens={dados.maiores_quedas} />
      </div>
    </div>
  );
}

function Secao({ titulo, itens }: { titulo: string; itens: any[] }) {
  if (!itens || itens.length === 0) return null;
  return (
    <section>
      <h2 className="text-lg font-semibold mb-3">{titulo}</h2>
      <div className="flex gap-3 overflow-x-auto pb-2">
        {itens.map((q) => <QuoteCard key={q.ticker} q={q} />)}
      </div>
    </section>
  );
}
