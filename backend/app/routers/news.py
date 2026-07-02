from fastapi import APIRouter, HTTPException
from ..services import yahoo, gemini

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/{ticker}")
def get_news(ticker: str):
    try:
        raw_news = yahoo.get_news(ticker)
        if not raw_news:
            return {"noticias": []}

        analysis = gemini.analyze_news(ticker, raw_news)
        out = []
        for i, n in enumerate(raw_news):
            extra = analysis[i] if i < len(analysis) and isinstance(analysis[i], dict) else {}
            out.append({**n, **extra})
        return {"noticias": out}
    except RuntimeError as e:
        # sem chave de API configurada -> devolve notícias sem análise de IA
        return {"noticias": raw_news, "aviso": str(e)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter notícias: {e}")
