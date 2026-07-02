const MAPA: Record<string, { emoji: string; cor: string }> = {
  "Forte Compra": { emoji: "🟢", cor: "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300" },
  "Compra": { emoji: "🟢", cor: "bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300" },
  "Manter": { emoji: "🟡", cor: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300" },
  "Venda": { emoji: "🟠", cor: "bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300" },
  "Forte Venda": { emoji: "🔴", cor: "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300" },
};

export default function RecomendacaoBadge({ recomendacao }: { recomendacao: string }) {
  const info = MAPA[recomendacao] || { emoji: "⚪", cor: "bg-slate-100 text-slate-700" };
  return <span className={`badge text-sm ${info.cor}`}>{info.emoji} {recomendacao}</span>;
}
