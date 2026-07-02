"""
Sistema de pontuação (0-100) de cada ativo.
Pesos conforme especificação:
  Indicadores técnicos      25%
  Indicadores fundamentais  25%
  Sentimento das notícias   20%
  Volume                    10%
  Volatilidade              10%
  Crescimento histórico     10%
"""
import numpy as np


def _rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def _sma(closes, period):
    if len(closes) < period:
        return None
    return float(np.mean(closes[-period:]))


def technical_score(history: list) -> dict:
    closes = [h["fecho"] for h in history if h.get("fecho") is not None]
    if len(closes) < 20:
        return {"pontos": 50, "detalhe": "Histórico insuficiente para análise técnica robusta."}

    rsi = _rsi(closes)
    sma20 = _sma(closes, 20)
    sma50 = _sma(closes, min(50, len(closes)))
    preco_atual = closes[-1]

    pontos = 50
    motivos = []

    if rsi is not None:
        if rsi < 30:
            pontos += 15
            motivos.append(f"RSI em {rsi:.0f} sugere sobrevenda (possível oportunidade de compra).")
        elif rsi > 70:
            pontos -= 15
            motivos.append(f"RSI em {rsi:.0f} sugere sobrecompra (risco de correção).")
        else:
            motivos.append(f"RSI em {rsi:.0f}, em zona neutra.")

    if sma20 and sma50:
        if preco_atual > sma20 > sma50:
            pontos += 15
            motivos.append("Preço acima das médias móveis de curto e médio prazo — tendência de alta.")
        elif preco_atual < sma20 < sma50:
            pontos -= 15
            motivos.append("Preço abaixo das médias móveis — tendência de baixa.")
        else:
            motivos.append("Sinal misto entre médias móveis de curto e médio prazo.")

    pontos = max(0, min(100, pontos))
    return {"pontos": pontos, "rsi": rsi, "sma20": sma20, "sma50": sma50, "detalhe": " ".join(motivos)}


def fundamental_score(info: dict) -> dict:
    pontos = 50
    motivos = []

    pe = info.get("pe_ratio")
    if pe is not None:
        if 0 < pe < 15:
            pontos += 15
            motivos.append(f"P/E de {pe:.1f} é relativamente baixo, sugerindo preço atrativo face aos lucros.")
        elif pe > 40:
            pontos -= 10
            motivos.append(f"P/E de {pe:.1f} é elevado, indicando expectativas de crescimento já refletidas no preço.")

    crescimento = info.get("crescimento_receita")
    if crescimento is not None:
        if crescimento > 0.1:
            pontos += 10
            motivos.append(f"Crescimento de receita de {crescimento*100:.1f}% reforça a saúde do negócio.")
        elif crescimento < 0:
            pontos -= 10
            motivos.append("Receita em contração no último período.")

    margem = info.get("margem_lucro")
    if margem is not None:
        if margem > 0.15:
            pontos += 10
            motivos.append(f"Margem de lucro saudável de {margem*100:.1f}%.")
        elif margem < 0:
            pontos -= 15
            motivos.append("Empresa com margens de lucro negativas.")

    pontos = max(0, min(100, pontos))
    if not motivos:
        motivos.append("Dados fundamentais insuficientes para uma análise completa.")
    return {"pontos": pontos, "detalhe": " ".join(motivos)}


def volume_score(history: list) -> dict:
    vols = [h["volume"] for h in history if h.get("volume")]
    if len(vols) < 10:
        return {"pontos": 50, "detalhe": "Dados de volume insuficientes."}
    media = np.mean(vols[:-1]) if len(vols) > 1 else vols[-1]
    atual = vols[-1]
    if media == 0:
        return {"pontos": 50, "detalhe": "Volume médio indisponível."}
    ratio = atual / media
    if ratio > 1.5:
        return {"pontos": 75, "detalhe": f"Volume atual {ratio:.1f}x acima da média — forte interesse do mercado."}
    if ratio < 0.5:
        return {"pontos": 40, "detalhe": "Volume abaixo da média — baixa liquidez recente."}
    return {"pontos": 55, "detalhe": "Volume dentro da normalidade."}


def volatility_score(history: list) -> dict:
    closes = [h["fecho"] for h in history if h.get("fecho") is not None]
    if len(closes) < 10:
        return {"pontos": 50, "detalhe": "Dados insuficientes para calcular volatilidade."}
    returns = np.diff(closes) / closes[:-1]
    vol = float(np.std(returns) * np.sqrt(252) * 100)  # volatilidade anualizada %
    if vol < 20:
        pontos = 75
        nivel = "baixa"
    elif vol < 40:
        pontos = 55
        nivel = "moderada"
    else:
        pontos = 35
        nivel = "elevada"
    return {"pontos": pontos, "volatilidade_pct": round(vol, 1), "detalhe": f"Volatilidade anualizada {nivel} ({vol:.1f}%)."}


def growth_score(history: list) -> dict:
    closes = [h["fecho"] for h in history if h.get("fecho") is not None]
    if len(closes) < 20:
        return {"pontos": 50, "detalhe": "Histórico insuficiente para avaliar crescimento."}
    variacao = (closes[-1] - closes[0]) / closes[0] * 100
    if variacao > 20:
        pontos = 80
    elif variacao > 0:
        pontos = 60
    elif variacao > -20:
        pontos = 40
    else:
        pontos = 20
    return {"pontos": pontos, "variacao_periodo_pct": round(variacao, 1), "detalhe": f"Variação de {variacao:.1f}% no período analisado."}


def news_sentiment_score(sentiment_label: str) -> dict:
    mapa = {"Positiva": 80, "Neutra": 55, "Negativa": 30}
    pontos = mapa.get(sentiment_label, 50)
    return {"pontos": pontos, "detalhe": f"Sentimento geral das notícias: {sentiment_label}."}


def compute_total_score(history: list, info: dict, sentiment_label: str = "Neutra") -> dict:
    tech = technical_score(history)
    fund = fundamental_score(info)
    vol = volume_score(history)
    volat = volatility_score(history)
    growth = growth_score(history)
    news = news_sentiment_score(sentiment_label)

    total = (
        tech["pontos"] * 0.25
        + fund["pontos"] * 0.25
        + news["pontos"] * 0.20
        + vol["pontos"] * 0.10
        + volat["pontos"] * 0.10
        + growth["pontos"] * 0.10
    )
    total = round(total, 1)

    if total >= 95:
        classificacao = "Excelente oportunidade"
    elif total >= 80:
        classificacao = "Boa oportunidade"
    elif total >= 65:
        classificacao = "Interessante"
    elif total >= 50:
        classificacao = "Neutro"
    else:
        classificacao = "Elevado risco"

    return {
        "pontuacao_total": total,
        "classificacao": classificacao,
        "componentes": {
            "tecnico": tech,
            "fundamental": fund,
            "sentimento_noticias": news,
            "volume": vol,
            "volatilidade": volat,
            "crescimento": growth,
        },
        "pesos": {
            "tecnico": 25, "fundamental": 25, "sentimento_noticias": 20,
            "volume": 10, "volatilidade": 10, "crescimento": 10,
        },
    }
