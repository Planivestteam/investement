import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .routers import assets, search, news, score, ai, dashboard

load_dotenv()

app = FastAPI(
    title="Plataforma de Consultoria Financeira com IA",
    description="API que fornece dados reais do Yahoo Finance e análises geradas por IA (Claude), em português europeu.",
    version="1.0.0",
)

frontend_origin = os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)
app.include_router(assets.router)
app.include_router(search.router)
app.include_router(news.router)
app.include_router(score.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {"status": "ok", "mensagem": "API da Plataforma de Consultoria Financeira com IA está a funcionar."}


@app.get("/api/health")
def health():
    return {"status": "healthy"}
