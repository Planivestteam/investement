"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import PriceChart from "@/components/PriceChart";
import NewsCard from "@/components/NewsCard";
import AIAnalysis from "@/components/AIAnalysis";
import ScoreBadge from "@/components/ScoreBadge";

export default function AtivoPage() {
  const params = useParams();
  const ticker = decodeURIComponent(params.ticker as string);

  const [ativo, setAtivo] = useState<any>(null);
  const [score, setScore] = useState<any>(null);
  const [noticias, setNoticias] = useState<any[]>([]);
  const [analise, setAnalise] = useState<any>(null);
  const [aLoading, setALoading] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    setErro(null);
    api.asset(ticker).then(setAtivo).catch((e) => setErro(e.message));
    api.score(ticker).then(setScore).catch(() => {});
    api.news(ticker).then((d) => setNoticias(d.noticias || [])).catch(() => {});
  }, [ticker]);

  async function pedirAnalise() {
    setALoading(true);
    try {
      const d = await api.analyze(ticker);
      setAnalise(d.analise);
    } catch (e: any) {
      setAnalise({ erro: e.message });
    } finally {
      setALoading(false);
    }
  }

  if (erro) return <div className="text-red-600">Erro: {erro}</div>;
  if (!ativo) return <div className="text-slate-500">A carregar {ticker}...</div>;

  const q = ativo.cotacao;
  const info = ativo.fundamentais;
  const positivo = (q.variacao_pct ?? 0) >= 0;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">{info.nome || q.ticker} <span className="text-slate-400 text-lg">({q.ticker})</span></h1>
          {info.setor && <p className="text-sm text-slate-500">{info.setor} · {info.industria}</p>}
        </div>
        {score && <ScoreBadge pontuacao={score.pontuacao_total} classificacao={score.classificacao} />}
      </div>

      <div className="flex items-baseline gap-3">
        <span className="text-4xl font-bold">{q.preco?.toLocaleString("pt-PT", { maximumFractionDigits: 2 })}</span>
        <span className={`text-lg font-medium ${positivo ? "text-subida" : "text-descida"}`}>
          {positivo ? "▲" : "▼"} {Math.abs(q.variacao_pct ?? 0).toFixed(2)}% ({q.moeda})
        </span>
      </div>

      <div className="card">
        <PriceChart historico={ativo.historico} />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
        <Metric label="Capitalização" value={formatBig(q.capitalizacao)} />
        <Metric label="Volume" value={formatBig(q.volume)} />
        <Metric label="Máx. 52 semanas" value={q.maximo_52s} />
        <Metric label="Mín. 52 semanas" value={q.minimo_52s} />
        <Metric label="P/E" value={info.pe_ratio?.toFixed?.(2)} />
        <Metric label="EPS" value={info.eps} />
        <Metric label="Dividend Yield" value={info.dividend_yield ? `${(info.dividend_yield * 100).toFixed(2)}%` : null} />
        <Metric label="Beta" value={info.beta} />
      </div>

      <div>
        {!analise && (
          <button
            onClick={pedirAnalise}
            disabled={aLoading}
            className="px-4 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
          >
            {aLoading ? "A analisar com IA..." : "🤖 Gerar Análise de IA"}
          </button>
        )}
        {analise && <AIAnalysis analise={analise} />}
      </div>

      <section>
        <h2 className="text-lg font-semibold mb-3">Notícias Recentes</h2>
        {noticias.length === 0 ? (
          <p className="text-sm text-slate-500">Sem notícias recentes disponíveis para este ativo.</p>
        ) : (
          <div className="grid md:grid-cols-2 gap-3">
            {noticias.map((n, i) => <NewsCard key={i} n={n} />)}
          </div>
        )}
      </section>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: any }) {
  return (
    <div className="card">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="font-semibold">{value ?? "—"}</div>
    </div>
  );
}

function formatBig(n: number | null | undefined) {
  if (n == null) return null;
  if (n >= 1e12) return (n / 1e12).toFixed(2) + "T";
  if (n >= 1e9) return (n / 1e9).toFixed(2) + "B";
  if (n >= 1e6) return (n / 1e6).toFixed(2) + "M";
  return n.toLocaleString("pt-PT");
}
