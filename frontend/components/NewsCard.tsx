const CORES: Record<string, string> = {
  Positiva: "text-green-600 dark:text-green-400",
  Negativa: "text-red-600 dark:text-red-400",
  Neutra: "text-slate-500",
};

export default function NewsCard({ n }: { n: any }) {
  return (
    <div className="card">
      <div className="flex justify-between items-start gap-2">
        <a href={n.link} target="_blank" rel="noopener noreferrer" className="font-medium hover:underline">
          {n.titulo}
        </a>
        {n.sentimento && (
          <span className={`text-xs font-semibold whitespace-nowrap ${CORES[n.sentimento] || "text-slate-500"}`}>
            {n.sentimento}
          </span>
        )}
      </div>
      <div className="text-xs text-slate-500 mt-1">
        {n.fonte} {n.data ? `· ${n.data}` : ""}
      </div>
      {n.impacto_esperado && (
        <p className="text-sm mt-2 text-slate-700 dark:text-slate-300">{n.impacto_esperado}</p>
      )}
      {(n.prazo || n.importancia || n.confianca) && (
        <div className="flex gap-2 mt-2 text-xs text-slate-500">
          {n.prazo && <span>Prazo: {n.prazo}</span>}
          {n.importancia && <span>· Importância: {n.importancia}</span>}
          {n.confianca && <span>· Confiança: {n.confianca}</span>}
        </div>
      )}
    </div>
  );
}
