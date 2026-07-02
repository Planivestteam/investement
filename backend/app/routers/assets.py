from fastapi import APIRouter, HTTPException, Query
from ..services import yahoo

router = APIRouter(prefix="/api/asset", tags=["assets"])


@router.get("/{ticker}")
def get_asset(ticker: str, period: str = Query("1y"), interval: str = Query("1d")):
    try:
        quote = yahoo.get_quote(ticker)
        info = yahoo.get_info(ticker)
        history = yahoo.get_history(ticker, period=period, interval=interval)
        dividends = yahoo.get_dividends(ticker)
        earnings = yahoo.get_earnings(ticker)

        if quote.get("preco") is None and not history:
            raise HTTPException(status_code=404, detail=f"Ativo '{ticker}' não encontrado.")

        return {
            "cotacao": quote,
            "fundamentais": info,
            "historico": history,
            "dividendos": dividends,
            "resultados": earnings,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados: {e}")


@router.get("/{ticker}/historico")
def get_history_only(ticker: str, period: str = "1y", interval: str = "1d"):
    return {"historico": yahoo.get_history(ticker, period=period, interval=interval)}
