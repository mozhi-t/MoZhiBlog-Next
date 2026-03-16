"""
Simple in-memory cache with TTL support.
"""
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from time import time
from typing import Any

from logger import logger


DEFAULT_CACHE_TTL_SECONDS = 60


@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class MemoryCache:
    def __init__(self) -> None:
        self._store: dict[str, CacheEntry] = {}
        self._lock = RLock()

    def get(self, key: str) -> Any | None:
        with self._lock:
            entry = self._store.get(key)
            if not entry:
                logger.debug(f"cache miss - key: {key}")
                return None

            if entry.expires_at <= time():
                self._store.pop(key, None)
                logger.debug(f"cache expired - key: {key}")
                return None

            logger.debug(f"cache hit - key: {key}")
            return entry.value

    def set(self, key: str, value: Any, ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS) -> Any:
        with self._lock:
            self._store[key] = CacheEntry(
                value=value,
                expires_at=time() + ttl_seconds,
            )
            logger.debug(f"cache set - key: {key}, ttl: {ttl_seconds}s")
            return value

    def delete(self, key: str) -> None:
        with self._lock:
            existed = self._store.pop(key, None)
            if existed is not None:
                logger.debug(f"cache delete - key: {key}")

    def delete_prefix(self, prefix: str) -> None:
        with self._lock:
            keys = [key for key in self._store if key.startswith(prefix)]
            for key in keys:
                self._store.pop(key, None)
            if keys:
                logger.debug(f"cache delete prefix - prefix: {prefix}, count: {len(keys)}")

    def get_or_set(self, key: str, factory, ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS):
        cached = self.get(key)
        if cached is not None:
            return cached

        value = factory()
        return self.set(key, value, ttl_seconds)


cache = MemoryCache()
