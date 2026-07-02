from pydantic import BaseModel
from typing import Optional, List, Any


class NewsItem(BaseModel):
    titulo: str
    resumo: Optional[str] = None
    fonte: Optional[str] = None
    data: Optional[str] = None
    link: Optional[str] = None
    sentimento: Optional[str] = None  # Positiva / Negativa / Neutra
    impacto: Optional[str] = None
    prazo: Optional[str] = None
    importancia: Optional[str] = None
    confianca: Optional[str] = None


class InvestorProfile(BaseModel):
    idade: Optional[int] = None
    objetivo: Optional[str] = None
    capital: Optional[float] = None
    horizonte: Optional[str] = None
    experiencia: Optional[str] = None
    tolerancia_risco: Optional[str] = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    mensagens: List[ChatMessage]
    perfil: Optional[InvestorProfile] = None
