"use client";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Filler,
} from "chart.js";

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Filler);

export default function PriceChart({ historico }: { historico: any[] }) {
  if (!historico || historico.length === 0) {
    return <div className="text-sm text-slate-500">Sem dados históricos disponíveis.</div>;
  }
  const labels = historico.map((h) => h.data);
  const precos = historico.map((h) => h.fecho);
  const subiu = precos[precos.length - 1] >= precos[0];

  const data = {
    labels,
    datasets: [
      {
        label: "Fecho",
        data: precos,
        borderColor: subiu ? "#16a34a" : "#dc2626",
        backgroundColor: subiu ? "rgba(22,163,74,0.08)" : "rgba(220,38,38,0.08)",
        fill: true,
        tension: 0.25,
        pointRadius: 0,
        borderWidth: 2,
      },
    ],
  };

  const options: any = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { ticks: { maxTicksLimit: 8, color: "#64748b" }, grid: { display: false } },
      y: { ticks: { color: "#64748b" }, grid: { color: "rgba(148,163,184,0.15)" } },
    },
  };

  return (
    <div className="h-72">
      <Line data={data} options={options} />
    </div>
  );
}
