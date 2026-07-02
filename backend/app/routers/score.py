from fastapi import APIRouter, HTTPException
from ..services import yahoo, scoring

router = APIRouter(prefix="/api/score", tags=["score"])


@router.get("/{ticker}")
def get_score(ticker: str):
    try:
        info = yahoo.get_info(ticker)
        history = yahoo.get_history(ticker, period="6mo", interval="1d")
        if not history:
            raise HTTPException(status_code=404, detail="Histórico insuficiente para calcular pontuação.")
        result = scoring.compute_total_score(history, info)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular pontuação: {e}")
