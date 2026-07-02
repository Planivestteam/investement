"""
Cache inteligente em memória com TTL (time-to-live).
Reduz o número de pedidos ao Yahoo Finance e mantém a app rápida.
Para produção multi-instância, substituir por Redis (a interface mantém-se igual).
"""
from cachetools import TTLCache
from typing import Any, Callable
import threading

_lock = threading.Lock()

# Caches com diferentes TTLs consoante a volatilidade dos dados
_price_cache = TTLCache(maxsize=2000, ttl=30)        # preços: 30s
_info_cache = TTLCache(maxsize=1000, ttl=60 * 30)    # fundamentais: 30min
_news_cache = TTLCache(maxsize=1000, ttl=60 * 10)    # notícias: 10min
_history_cache = TTLCache(maxsize=1000, ttl=60 * 5)  # histórico: 5min


def cached(cache: TTLCache, key: str, fetch_fn: Callable[[], Any]) -> Any:
    with _lock:
        if key in cache:
            return cache[key]
    value = fetch_fn()
    with _lock:
        cache[key] = value
    return value


def get_price_cache():
    return _price_cache


def get_info_cache():
    return _info_cache


def get_news_cache():
    return _news_cache


def get_history_cache():
    return _history_cache
