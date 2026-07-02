export default function ScoreBadge({ pontuacao, classificacao }: { pontuacao: number; classificacao: string }) {
  const cor =
    pontuacao >= 80 ? "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300" :
    pontuacao >= 65 ? "bg-lime-100 text-lime-800 dark:bg-lime-900/40 dark:text-lime-300" :
    pontuacao >= 50 ? "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300" :
    "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300";

  return (
    <div className={`badge ${cor}`}>
      {pontuacao.toFixed(0)}/100 · {classificacao}
    </div>
  );
}
