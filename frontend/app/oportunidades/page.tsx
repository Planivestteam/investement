"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import Link from "next/link";
import ScoreBadge from "@/components/ScoreBadge";

const LISTA_ACOES = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "JPM", "V", "JNJ"];
const LISTA_CRIPTO = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "ADA-USD"];

export default function OportunidadesPage() {
  const [acoes, setAcoes] = useState<any[]>([]);
  const [cripto, setCripto] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function carregar() {
      const a = await Promise.all(LISTA_ACOES.map((t) => api.score(t).then((s) => ({ ticker: t, ...s })).catch(() => null)));
      const c = await Promise.all(LISTA_CRIPTO.map((t) => api.score(t).then((s) => ({ ticker: t, ...s })).catch(() => null)));
      setAcoes(a.filter(Boolean).sort((x, y) => y.pontuacao_total - x.pontuacao_total));
      setCripto(c.filter(Boolean).sort((x, y) => y.pontuacao_total - x.pontuacao_total));
      setLoading(false);
    }
    carregar();
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Oportunidades de Hoje</h1>
        <p className="text-sm text-slate-500 mt-1">
          Pontuação calculada com base em indicadores técnicos (25%), fundamentais (25%), sentimento das
          notícias (20%), volume (10%), volatilidade (10%) e crescimento histórico (10%).
        </p>
      </div>

      {loading && <p className="text-slate-500">A calcular pontuações...</p>}

      {!loading && (
        <>
          <Lista titulo="Melhores Ações" itens={acoes} />
          <Lista titulo="Melhores Criptomoedas" itens={cripto} />
        </>
      )}
    </div>
  );
}

function Lista({ titulo, itens }: { titulo: string; itens: any[] }) {
  if (itens.length === 0) return null;
  return (
    <section>
      <h2 className="text-lg font-semibold mb-3">{titulo}</h2>
      <div className="grid md:grid-cols-2 gap-3">
        {itens.map((item) => (
          <Link key={item.ticker} href={`/ativo/${item.ticker}`} className="card flex items-center justify-between hover:shadow-md">
            <span className="font-medium">{item.ticker}</span>
            <ScoreBadge pontuacao={item.pontuacao_total} classificacao={item.classificacao} />
          </Link>
        ))}
      </div>
    </section>
  );
}
