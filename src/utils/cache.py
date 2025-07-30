"""Cache Service"""
import json
from typing import Any, Optional

class CacheService:
    """Simple in-memory cache for development"""
    def __init__(self):
        self._cache = {}
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self._cache:
            return self._cache[key]
        return None
    
    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in cache"""
        self._cache[key] = value
    
    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        if key in self._cache:
            del self._cache[key]

# Global cache instance
cache_service = CacheService()
