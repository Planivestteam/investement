from fastapi import APIRouter
from ..services import yahoo, gemini

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

INDICES = ["^GSPC", "^IXIC", "^DJI", "^FTSE", "^GDAXI", "^N225", "PSI20.LS"]
CRIPTO = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD"]
ACOES_DESTAQUE = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"]
COMMODITIES = ["GC=F", "CL=F", "SI=F"]
FOREX = ["EURUSD=X", "GBPUSD=X", "USDJPY=X"]


def _quotes(tickers):
    out = []
    for tk in tickers:
        try:
            q = yahoo.get_quote(tk)
            out.append(q)
        except Exception:
            continue
    return out


@router.get("")
def get_dashboard():
    indices = _quotes(INDICES)
    cripto = _quotes(CRIPTO)
    acoes = _quotes(ACOES_DESTAQUE)
    commodities = _quotes(COMMODITIES)
    forex = _quotes(FOREX)

    todos = indices + cripto + acoes
    com_variacao = [a for a in todos if a.get("variacao_pct") is not None]
    maiores_subidas = sorted(com_variacao, key=lambda x: x["variacao_pct"], reverse=True)[:5]
    maiores_quedas = sorted(com_variacao, key=lambda x: x["variacao_pct"])[:5]

    resumo_ia = None
    try:
        resumo_ia = gemini.daily_summary({
            "indices": indices, "cripto": cripto, "maiores_subidas": maiores_subidas, "maiores_quedas": maiores_quedas,
        })
    except Exception:
        resumo_ia = None

    return {
        "indices": indices,
        "criptomoedas": cripto,
        "acoes_destaque": acoes,
        "commodities": commodities,
        "forex": forex,
        "maiores_subidas": maiores_subidas,
        "maiores_quedas": maiores_quedas,
        "resumo_ia": resumo_ia,
    }
