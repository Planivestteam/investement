import RecomendacaoBadge from "./RecomendacaoBadge";

export default function AIAnalysis({ analise }: { analise: any }) {
  if (!analise || analise.erro) {
    return (
      <div className="card text-sm text-slate-500">
        Análise de IA indisponível de momento. {analise?.erro ? `(${analise.erro})` : ""}
      </div>
    );
  }

  return (
    <div className="card space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <RecomendacaoBadge recomendacao={analise.recomendacao} />
        <span className="text-xs text-slate-500">Confiança: {analise.nivel_confianca}</span>
      </div>

      <p className="text-sm leading-relaxed">{analise.resumo}</p>

      <div className="grid grid-cols-2 gap-3">
        <div className="rounded-lg bg-green-50 dark:bg-green-900/20 p-3">
          <div className="text-xs text-green-700 dark:text-green-400 font-semibold">Probabilidade de subida</div>
          <div className="text-2xl font-bold text-green-700 dark:text-green-400">{analise.probabilidade_subida_pct}%</div>
        </div>
        <div className="rounded-lg bg-red-50 dark:bg-red-900/20 p-3">
          <div className="text-xs text-red-700 dark:text-red-400 font-semibold">Probabilidade de descida</div>
          <div className="text-2xl font-bold text-red-700 dark:text-red-400">{analise.probabilidade_descida_pct}%</div>
        </div>
      </div>

      <div>
        <h4 className="font-semibold text-sm mb-1">Porquê esta recomendação?</h4>
        <p className="text-sm text-slate-700 dark:text-slate-300">{analise.motivo_recomendacao}</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <h4 className="font-semibold text-sm mb-1 text-red-600">⚠ Riscos</h4>
          <ul className="text-sm list-disc list-inside space-y-1 text-slate-700 dark:text-slate-300">
            {(analise.riscos || []).map((r: string, i: number) => <li key={i}>{r}</li>)}
          </ul>
        </div>
        <div>
          <h4 className="font-semibold text-sm mb-1 text-green-600">✓ Oportunidades</h4>
          <ul className="text-sm list-disc list-inside space-y-1 text-slate-700 dark:text-slate-300">
            {(analise.oportunidades || []).map((o: string, i: number) => <li key={i}>{o}</li>)}
          </ul>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-4 text-sm">
        <p><b>Preço:</b> {analise.preco_avaliacao}</p>
        <p><b>Crescimento:</b> {analise.crescimento_empresa}</p>
        <p><b>Impacto das notícias:</b> {analise.impacto_noticias}</p>
        <p><b>Sentimento do mercado:</b> {analise.sentimento_mercado}</p>
        <p><b>Melhor prazo:</b> {analise.melhor_prazo}</p>
        <p><b>Perfil de investidor indicado:</b> {analise.perfil_investidor_indicado}</p>
      </div>

      <p className="text-xs text-slate-400 border-t border-slate-200 dark:border-slate-800 pt-3">
        {analise.aviso_legal}
      </p>
    </div>
  );
}
