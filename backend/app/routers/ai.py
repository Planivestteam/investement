from fastapi import APIRouter, HTTPException
from ..services import yahoo, scoring, claude
from ..models import ChatRequest

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.get("/analyze/{ticker}")
def analyze(ticker: str):
    try:
        quote = yahoo.get_quote(ticker)
        info = yahoo.get_info(ticker)
        history = yahoo.get_history(ticker, period="6mo", interval="1d")
        news = yahoo.get_news(ticker)

        if not history and quote.get("preco") is None:
            raise HTTPException(status_code=404, detail=f"Ativo '{ticker}' não encontrado.")

        score = scoring.compute_total_score(history, info) if history else None
        closes = [h["fecho"] for h in history if h.get("fecho")]
        history_summary = {
            "num_pontos": len(closes),
            "preco_inicial_periodo": closes[0] if closes else None,
            "preco_final_periodo": closes[-1] if closes else None,
            "maximo_periodo": max(closes) if closes else None,
            "minimo_periodo": min(closes) if closes else None,
        }

        analysis = claude.analyze_asset(ticker, quote, info, history_summary, news, score)
        return {"analise": analysis, "pontuacao": score}
    except HTTPException:
        raise
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise de IA: {e}")


@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    try:
        resposta = claude.chat(
            [m.model_dump() for m in req.mensagens],
            req.perfil.model_dump() if req.perfil else None,
        )
        return {"resposta": resposta}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no assistente: {e}")


@router.post("/comparar")
def compare(tickers: list[str]):
    if len(tickers) < 2 or len(tickers) > 5:
        raise HTTPException(status_code=400, detail="Fornece entre 2 e 5 tickers para comparar.")
    try:
        contexto = []
        for tk in tickers:
            quote = yahoo.get_quote(tk)
            info = yahoo.get_info(tk)
            history = yahoo.get_history(tk, period="6mo")
            score = scoring.compute_total_score(history, info) if history else None
            contexto.append({"ticker": tk, "cotacao": quote, "fundamentais": info, "pontuacao": score})
        resposta = claude.compare_assets(contexto)
        return {"comparacao": resposta, "dados": contexto}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na comparação: {e}")
