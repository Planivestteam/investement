# 📈 ConsultorIA — Plataforma de Consultoria Financeira com IA

Plataforma web que combina dados reais do **Yahoo Finance** com análises geradas por **Inteligência
Artificial (Claude)**, em português europeu: dashboard de mercado, página de ativo, notícias com
classificação de sentimento, sistema de pontuação (0–100), "Oportunidades de Hoje" e análise de IA
com recomendação, probabilidades e explicação justificada.

> **Nota honesta:** este repositório é uma base sólida e funcional (MVP) que cobre os pilares
> principais do pedido original (dashboard, pesquisa, página de ativo, IA, notícias, scoring,
> oportunidades diárias). Funcionalidades mais avançadas do pedido original — carteira virtual,
> simulador histórico completo, comparador visual, alertas automáticos, autenticação OAuth,
> PostgreSQL/Prisma — estão desenhadas na arquitetura mas ainda por implementar. O código está
> organizado para que as acrescentes facilmente (ver secção "Próximos Passos").

---

## 🗂 Estrutura

```
fin-ai-platform/
├── backend/           # FastAPI (Python) — dados Yahoo Finance + IA
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/   # endpoints: dashboard, asset, search, news, score, ai
│   │   └── services/  # yahoo.py, scoring.py, claude.py, cache.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/          # Next.js 14 + TypeScript + Tailwind
│   ├── app/            # dashboard, /ativo/[ticker], /oportunidades
│   ├── components/
│   ├── lib/api.ts
│   ├── Dockerfile
│   └── .env.example
└── docker-compose.yml  # correr tudo localmente com um comando
```

---

## ▶️ Correr localmente

### Opção A — Docker (recomendado)

```bash
cp backend/.env.example backend/.env
# edita backend/.env e coloca a tua ANTHROPIC_API_KEY

docker compose up --build
```

- Frontend: http://localhost:3000
- Backend/API: http://localhost:8000/docs (Swagger automático)

### Opção B — Manual

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # e edita a chave da API
uvicorn app.main:app --reload --port 8000

# Frontend (noutro terminal)
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

---

## 🔑 Chave da Anthropic (Claude)

As funcionalidades de IA (análise de ativos, notícias com sentimento, resumo diário, chat) exigem
uma chave da API em `backend/.env`:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
CLAUDE_MODEL=claude-sonnet-5
```

Sem a chave, a app continua a funcionar (preços, gráficos, fundamentais, notícias em bruto), mas
as secções de IA mostram um aviso de indisponibilidade em vez de inventarem conteúdo — por
desenho, a IA nunca deve simular dados que não tem.

---

## 🐙 Colocar no GitHub

```bash
cd fin-ai-platform
git init
git add .
git commit -m "Plataforma de consultoria financeira com IA - versão inicial"
git branch -M main
git remote add origin https://github.com/SEU-UTILIZADOR/SEU-REPOSITORIO.git
git push -u origin main
```

⚠️ O ficheiro `.gitignore` já exclui `.env` — nunca faças commit da tua chave da Anthropic.

---

## 🚂 Deploy no Railway

O Railway lê o repositório e cria **dois serviços** (backend e frontend), cada um com o seu
`Dockerfile`. Passos:

1. Vai a [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo** →
   seleciona este repositório.
2. Railway vai perguntar qual a pasta raiz do serviço. Cria **dois serviços** a partir do mesmo
   repo:
   - **Serviço 1 — Backend**: em *Settings → Root Directory* define `backend`. O Railway deteta o
     `Dockerfile` automaticamente.
   - **Serviço 2 — Frontend**: em *Settings → Root Directory* define `frontend`.
3. Configura as variáveis de ambiente em cada serviço (*Variables*):

   **Backend**
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   CLAUDE_MODEL=claude-sonnet-5
   FRONTEND_ORIGIN=https://<url-publica-do-frontend>.up.railway.app
   ```
   (O Railway define `PORT` automaticamente — o `Dockerfile` já usa `$PORT`.)

   **Frontend**
   ```
   NEXT_PUBLIC_API_URL=https://<url-publica-do-backend>.up.railway.app
   ```
4. Em cada serviço, ativa **Generate Domain** (Settings → Networking) para obteres o URL público.
5. Depois de teres o URL do backend, atualiza `NEXT_PUBLIC_API_URL` no frontend e faz redeploy
   (o Railway faz isto automaticamente a cada `git push`).

Alternativa: usar a CLI do Railway (`railway up`) dentro de cada pasta (`backend/` e `frontend/`)
em vez do dashboard.

---

## 🧭 Próximos Passos (para expandir para a visão completa do briefing)

- **Carteira virtual + PostgreSQL/Prisma**: adicionar modelo de utilizador, autenticação
  (JWT/OAuth Google) e tabelas de posições/transações.
- **Simulador histórico** ("se tivesse investido X há Y anos"): endpoint que usa
  `yahoo.get_history` com período longo e calcula CAGR, comparação com S&P 500/Bitcoin/inflação.
- **Comparador visual**: página `/comparar` que chama `POST /api/ai/comparar` (já implementado no
  backend) e mostra tabela + gráfico lado a lado.
- **Perfil do investidor**: formulário que guarda em `localStorage`/BD e é enviado em
  `perfil` no chat e na análise de IA (o backend já aceita este campo).
- **Assistente em chat**: página `/assistente` com histórico de mensagens a chamar
  `POST /api/ai/chat` (endpoint já implementado).
- **Alertas**: job periódico (cron/Celery) que compara `get_quote` guardado vs atual e dispara
  notificações (email/websocket) quando ultrapassa limiares.
- **Cache distribuído**: substituir `cachetools` (em memória) por Redis quando escalares para
  múltiplas instâncias.
- **Notícias em português**: o backend já traduz/analisa via Claude; podes reforçar priorizando
  fontes lusófonas (ex.: filtrar `fonte` por domínio `.pt`) antes de traduzir.

---

## ⚖️ Aviso Legal

Esta plataforma é uma ferramenta educativa e informativa. As análises geradas por IA são
estimativas baseadas em dados históricos e públicos — **não constituem aconselhamento financeiro**
nem garantem resultados futuros.
