"""
Serviço de acesso ao Yahoo Finance (via yfinance).
Todos os dados aqui são REAIS — nunca inventados. Se um campo não existir,
devolve-se None e o frontend/IA deve assumir "dado indisponível".
"""
import yfinance as yf
import pandas as pd
from datetime import datetime
from .cache import cached, get_price_cache, get_info_cache, get_news_cache, get_history_cache


def _safe(d: dict, key: str):
    v = d.get(key)
    if v is None:
        return None
    try:
        if isinstance(v, float) and (v != v):  # NaN check
            return None
    except Exception:
        pass
    return v


def get_quote(ticker: str) -> dict:
    def fetch():
        t = yf.Ticker(ticker)
        info = t.fast_info
        try:
            price = float(info.last_price)
        except Exception:
            price = None
        try:
            prev_close = float(info.previous_close)
        except Exception:
            prev_close = None
        change = None
        change_pct = None
        if price is not None and prev_close:
            change = price - prev_close
            change_pct = (change / prev_close) * 100

        return {
            "ticker": ticker.upper(),
            "preco": price,
            "fecho_anterior": prev_close,
            "variacao": change,
            "variacao_pct": change_pct,
            "moeda": getattr(info, "currency", None),
            "volume": getattr(info, "last_volume", None),
            "capitalizacao": getattr(info, "market_cap", None),
            "maximo_dia": getattr(info, "day_high", None),
            "minimo_dia": getattr(info, "day_low", None),
            "maximo_52s": getattr(info, "year_high", None),
            "minimo_52s": getattr(info, "year_low", None),
            "atualizado_em": datetime.utcnow().isoformat() + "Z",
        }

    return cached(get_price_cache(), f"quote:{ticker}", fetch)


def get_info(ticker: str) -> dict:
    def fetch():
        t = yf.Ticker(ticker)
        try:
            info = t.info
        except Exception:
            info = {}
        return {
            "nome": _safe(info, "longName") or _safe(info, "shortName"),
            "setor": _safe(info, "sector"),
            "industria": _safe(info, "industry"),
            "pais": _safe(info, "country"),
            "descricao": _safe(info, "longBusinessSummary"),
            "pe_ratio": _safe(info, "trailingPE"),
            "forward_pe": _safe(info, "forwardPE"),
            "eps": _safe(info, "trailingEps"),
            "dividend_yield": _safe(info, "dividendYield"),
            "payout_ratio": _safe(info, "payoutRatio"),
            "beta": _safe(info, "beta"),
            "receita": _safe(info, "totalRevenue"),
            "crescimento_receita": _safe(info, "revenueGrowth"),
            "margem_lucro": _safe(info, "profitMargins"),
            "divida_capital": _safe(info, "debtToEquity"),
            "roe": _safe(info, "returnOnEquity"),
            "empregados": _safe(info, "fullTimeEmployees"),
            "website": _safe(info, "website"),
            "logo": _safe(info, "logo_url"),
            "recomendacao_analistas": _safe(info, "recommendationKey"),
            "preco_alvo_medio": _safe(info, "targetMeanPrice"),
        }

    return cached(get_info_cache(), f"info:{ticker}", fetch)


def get_history(ticker: str, period: str = "1y", interval: str = "1d") -> list:
    def fetch():
        t = yf.Ticker(ticker)
        hist: pd.DataFrame = t.history(period=period, interval=interval)
        if hist is None or hist.empty:
            return []
        hist = hist.reset_index()
        date_col = "Date" if "Date" in hist.columns else "Datetime"
        out = []
        for _, row in hist.iterrows():
            out.append({
                "data": row[date_col].strftime("%Y-%m-%d %H:%M") if hasattr(row[date_col], "strftime") else str(row[date_col]),
                "abertura": round(float(row["Open"]), 4) if pd.notna(row["Open"]) else None,
                "maximo": round(float(row["High"]), 4) if pd.notna(row["High"]) else None,
                "minimo": round(float(row["Low"]), 4) if pd.notna(row["Low"]) else None,
                "fecho": round(float(row["Close"]), 4) if pd.notna(row["Close"]) else None,
                "volume": int(row["Volume"]) if "Volume" in row and pd.notna(row["Volume"]) else None,
            })
        return out

    return cached(get_history_cache(), f"hist:{ticker}:{period}:{interval}", fetch)


def get_dividends(ticker: str) -> list:
    def fetch():
        t = yf.Ticker(ticker)
        try:
            div = t.dividends
        except Exception:
            return []
        if div is None or div.empty:
            return []
        return [{"data": idx.strftime("%Y-%m-%d"), "valor": float(v)} for idx, v in div.tail(20).items()]

    return cached(get_info_cache(), f"div:{ticker}", fetch)


def get_earnings(ticker: str) -> list:
    def fetch():
        t = yf.Ticker(ticker)
        try:
            cal = t.earnings_dates
            if cal is None or cal.empty:
                return []
            cal = cal.reset_index()
            out = []
            for _, row in cal.head(8).iterrows():
                out.append({
                    "data": str(row.iloc[0]),
                    "eps_estimado": _safe(row.to_dict(), "EPS Estimate"),
                    "eps_real": _safe(row.to_dict(), "Reported EPS"),
                    "surpresa_pct": _safe(row.to_dict(), "Surprise(%)"),
                })
            return out
        except Exception:
            return []

    return cached(get_info_cache(), f"earn:{ticker}", fetch)


def get_news(ticker: str) -> list:
    def fetch():
        t = yf.Ticker(ticker)
        try:
            news = t.news or []
        except Exception:
            news = []
        out = []
        for n in news[:12]:
            content = n.get("content", n)  # yfinance mudou formato entre versões
            out.append({
                "titulo": content.get("title") or n.get("title"),
                "fonte": (content.get("provider") or {}).get("displayName") if isinstance(content.get("provider"), dict) else n.get("publisher"),
                "link": (content.get("canonicalUrl") or {}).get("url") if isinstance(content.get("canonicalUrl"), dict) else n.get("link"),
                "data": content.get("pubDate") or n.get("providerPublishTime"),
            })
        return out

    return cached(get_news_cache(), f"news:{ticker}", fetch)


def search_tickers(query: str) -> list:
    """Pesquisa de tickers. yfinance não tem endpoint oficial de search em todas as versões,
    por isso tentamos validar o próprio query como ticker e complementamos com uma lista popular."""
    query_up = query.strip().upper()
    results = []

    popular = {
        "APPLE": "AAPL", "MICROSOFT": "MSFT", "GOOGLE": "GOOGL", "ALPHABET": "GOOGL",
        "AMAZON": "AMZN", "TESLA": "TSLA", "META": "META", "NVIDIA": "NVDA",
        "BITCOIN": "BTC-USD", "ETHEREUM": "ETH-USD", "GALP": "GALP.LS", "EDP": "EDP.LS",
        "JERONIMO MARTINS": "JMT.LS", "SONAE": "SON.LS", "NETFLIX": "NFLX",
        "S&P 500": "^GSPC", "NASDAQ": "^IXIC", "OURO": "GC=F", "PETROLEO": "CL=F",
    }

    for name, tk in popular.items():
        if query_up in name or query_up in tk:
            results.append({"ticker": tk, "nome": name.title()})

    if query_up not in [r["ticker"] for r in results]:
        try:
            t = yf.Ticker(query_up)
            fi = t.fast_info
            if fi and getattr(fi, "last_price", None):
                results.insert(0, {"ticker": query_up, "nome": query_up})
        except Exception:
            pass

    return results[:10]
