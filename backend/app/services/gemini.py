"""
Serviço de Inteligência Artificial (Google Gemini API — nível gratuito).
Regra de ouro: a IA só pode usar os dados reais fornecidos no contexto.
É instruída explicitamente a nunca inventar dados nem notícias.

Usa o endpoint REST público da Gemini API (generativelanguage.googleapis.com),
sem SDK extra, apenas httpx (já é dependência do projeto).
Chave gratuita em: https://aistudio.google.com/apikey (sem cartão de crédito).
"""
import os
import json
import httpx

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# "gemini-flash-latest" aponta sempre para o modelo Flash estável mais recente da Google,
# que faz parte do nível gratuito da Gemini API.
MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

DISCLAIMER = (
    "Esta previsão é uma estimativa baseada em dados históricos, indicadores técnicos, "
    "indicadores fundamentais, sentimento das notícias e contexto do mercado. Não constitui "
    "aconselhamento financeiro nem garante resultados futuros."
)

SYSTEM_BASE = """És um consultor financeiro sénior que escreve exclusivamente em português europeu,
com linguagem clara e acessível mas tecnicamente rigorosa.

Regras absolutas:
- Usa APENAS os dados fornecidos no contexto (JSON). Nunca inventes preços, notícias, métricas ou factos.
- Se um dado não existir no contexto, diz explicitamente que não está disponível — não o inventes nem estimes livremente.
- Nunca apresentes previsões como certezas. Usa sempre linguagem de probabilidade/estimativa.
- Justifica sempre todas as conclusões e recomendações com base nos dados fornecidos.
- Termina qualquer análise preditiva com o aviso legal fornecido."""


def _require_key():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY não configurada no ambiente.")


def _call(system: str, user_content: str, max_tokens: int = 1500, json_mode: bool = False) -> str:
    """Chama a Gemini API (generateContent) com um único turno de utilizador + instrução de sistema."""
    _require_key()
    url = f"{BASE_URL}/{MODEL}:generateContent"
    headers = {"x-goog-api-key": GEMINI_API_KEY, "Content-Type": "application/json"}
    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user_content}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.4,
        },
    }
    if json_mode:
        body["generationConfig"]["responseMimeType"] = "application/json"

    with httpx.Client(timeout=60) as client:
        resp = client.post(url, headers=headers, json=body)
        if resp.status_code != 200:
            raise RuntimeError(f"Erro da Gemini API ({resp.status_code}): {resp.text[:300]}")
        data = resp.json()

    try:
        candidates = data.get("candidates", [])
        if not candidates:
            raise RuntimeError("A Gemini API não devolveu nenhuma resposta (possível bloqueio de segurança).")
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts)
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Não foi possível interpretar a resposta da Gemini API: {e}")


def _call_multiturn(system: str, messages: list, max_tokens: int = 1200) -> str:
    """Chama a Gemini API com histórico de conversa (para o chat)."""
    _require_key()
    url = f"{BASE_URL}/{MODEL}:generateContent"
    headers = {"x-goog-api-key": GEMINI_API_KEY, "Content-Type": "application/json"}

    contents = []
    for m in messages:
        role = "model" if m["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": contents,
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.5},
    }

    with httpx.Client(timeout=60) as client:
        resp = client.post(url, headers=headers, json=body)
        if resp.status_code != 200:
            raise RuntimeError(f"Erro da Gemini API ({resp.status_code}): {resp.text[:300]}")
        data = resp.json()

    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("A Gemini API não devolveu nenhuma resposta.")
    parts = candidates[0].get("content", {}).get("parts", [])
    return "".join(p.get("text", "") for p in parts).strip()


def analyze_asset(ticker: str, quote: dict, info: dict, history_summary: dict, news: list, score: dict) -> dict:
    """Gera análise completa + probabilidades + recomendação, em JSON estruturado."""
    context = {
        "ticker": ticker,
        "cotacao": quote,
        "fundamentais": info,
        "resumo_historico": history_summary,
        "noticias_recentes": news[:8],
        "pontuacao": score,
    }

    system = SYSTEM_BASE + """

Tarefa: produzir uma análise de investimento completa para o ativo fornecido.
Responde APENAS com um objeto JSON válido (sem markdown, sem ```), com exatamente estas chaves:

{
  "resumo": "resumo geral em 2-3 frases",
  "recomendacao": "Forte Compra" | "Compra" | "Manter" | "Venda" | "Forte Venda",
  "motivo_recomendacao": "explicação detalhada e justificada",
  "probabilidade_subida_pct": número entre 0 e 100,
  "probabilidade_descida_pct": número entre 0 e 100 (soma com o anterior deve dar 100),
  "nivel_confianca": "Alto" | "Médio" | "Baixo",
  "riscos": ["risco 1", "risco 2", "..."],
  "oportunidades": ["oportunidade 1", "oportunidade 2", "..."],
  "preco_avaliacao": "explicação se o preço parece barato ou caro e porquê",
  "crescimento_empresa": "análise sobre se a empresa/ativo continua a crescer",
  "impacto_noticias": "as notícias ajudam ou prejudicam o ativo, e porquê",
  "sentimento_mercado": "Otimista" | "Pessimista" | "Neutro",
  "melhor_prazo": "Curto Prazo" | "Longo Prazo" | "Ambos",
  "perfil_investidor_indicado": "descrição do perfil de investidor mais adequado",
  "aviso_legal": "%s"
}
""" % DISCLAIMER

    raw = _call(system, json.dumps(context, ensure_ascii=False, default=str), json_mode=True)
    return _safe_json(raw)


def analyze_news(ticker: str, news_items: list) -> list:
    """Classifica sentimento e explica impacto de cada notícia. Nunca inventa notícias."""
    if not news_items:
        return []

    system = SYSTEM_BASE + """

Tarefa: para cada notícia fornecida (já real, não inventes nenhuma nova), classifica o sentimento
e explica o impacto potencial no ativo. Responde APENAS com um array JSON, um objeto por notícia,
na MESMA ORDEM em que foram fornecidas, com as chaves:

{
  "sentimento": "Positiva" | "Negativa" | "Neutra",
  "impacto_esperado": "explicação curta do impacto potencial no preço",
  "prazo": "Curto Prazo" | "Longo Prazo",
  "importancia": "Alta" | "Média" | "Baixa",
  "confianca": "Alta" | "Média" | "Baixa"
}
"""
    payload = json.dumps({"ticker": ticker, "noticias": news_items}, ensure_ascii=False, default=str)
    raw = _call(system, payload, max_tokens=2000, json_mode=True)
    parsed = _safe_json(raw)
    return parsed if isinstance(parsed, list) else []


def daily_summary(market_snapshot: dict) -> str:
    system = SYSTEM_BASE + "\n\nTarefa: escreve um resumo diário de mercado em 4-6 frases, em português europeu, com base apenas nos dados fornecidos."
    return _call(system, json.dumps(market_snapshot, ensure_ascii=False, default=str), max_tokens=600)


def chat(messages: list, perfil: dict | None = None) -> str:
    system = SYSTEM_BASE + """

Estás a conversar diretamente com um utilizador num chat de assistente financeiro.
Responde de forma conversacional, útil e justificada, sempre em português europeu.
Se o utilizador pedir recomendações de investimento sem teres dados suficientes fornecidos
na conversa, explica que precisas de consultar dados reais (o utilizador pode pedir para
analisares um ativo específico pelo nome/ticker) em vez de inventares recomendações às cegas.
"""
    if perfil:
        system += f"\n\nPerfil do investidor: {json.dumps(perfil, ensure_ascii=False)}"

    return _call_multiturn(system, messages)


def compare_assets(assets_context: list) -> str:
    system = SYSTEM_BASE + """

Tarefa: compara os ativos fornecidos (até 5) e responde, em português europeu, de forma estruturada:
qual parece melhor investimento, qual tem menor risco, qual tem maior potencial, qual parece
sobrevalorizado e qual parece subvalorizado — sempre justificando com os dados fornecidos.
Termina com o aviso legal: """ + DISCLAIMER

    return _call(system, json.dumps(assets_context, ensure_ascii=False, default=str), max_tokens=1500)


def _safe_json(raw: str):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw)
    except Exception:
        return {"erro": "Não foi possível interpretar a resposta da IA.", "resposta_bruta": raw}
