from fastapi import APIRouter, Query
from ..services import yahoo

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("")
def search(q: str = Query(..., min_length=1)):
    return {"resultados": yahoo.search_tickers(q)}
