"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import SearchBar from "./SearchBar";

export default function Navbar() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const stored = typeof window !== "undefined" ? window.localStorage?.getItem("tema") : null;
    if (stored === "dark") {
      setDark(true);
      document.documentElement.classList.add("dark");
    }
  }, []);

  function toggleTema() {
    const novo = !dark;
    setDark(novo);
    document.documentElement.classList.toggle("dark", novo);
    try {
      window.localStorage.setItem("tema", novo ? "dark" : "light");
    } catch {}
  }

  return (
    <header className="sticky top-0 z-50 backdrop-blur bg-white/80 dark:bg-slate-950/80 border-b border-slate-200 dark:border-slate-800">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center gap-4">
        <Link href="/" className="font-bold text-lg tracking-tight whitespace-nowrap">
          📈 Consultor<span className="text-blue-600">IA</span>
        </Link>
        <nav className="hidden md:flex items-center gap-4 text-sm text-slate-600 dark:text-slate-300">
          <Link href="/">Dashboard</Link>
          <Link href="/oportunidades">Oportunidades de Hoje</Link>
        </nav>
        <div className="flex-1">
          <SearchBar />
        </div>
        <button
          onClick={toggleTema}
          className="px-3 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 text-sm"
        >
          {dark ? "☀️ Claro" : "🌙 Escuro"}
        </button>
      </div>
    </header>
  );
}
