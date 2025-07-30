"""Cache service for API responses"""
import json
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

class CacheService:
    """Simple in-memory cache (can be replaced with Redis later)"""
    
    def __init__(self):
        self._cache = {}
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self._cache:
            logger.debug(f"Cache hit: {key}")
            return self._cache[key]
        logger.debug(f"Cache miss: {key}")
        return None
    
    async def set(self, key: str, value: Any, expire: int = 300) -> None:
        """Set value in cache with expiration (in seconds)"""
        # For now, simple in-memory cache without expiration
        self._cache[key] = value
        logger.debug(f"Cache set: {key}")
    
    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache delete: {key}")
    
    async def clear(self) -> None:
        """Clear all cache"""
        self._cache.clear()
        logger.debug("Cache cleared")

# Create singleton instance
cache_service = CacheService()
