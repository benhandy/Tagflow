from typing import Any, Optional
import redis.asyncio as redis
from core.config import settings

class CacheService:
    def __init__(self):
        self.redis = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )
        
    async def get(self, key: str) -> Optional[Any]:
        return await self.redis.get(key)
        
    async def set(
        self,
        key: str,
        value: Any,
        expire: int = 3600
    ) -> None:
        await self.redis.set(key, value, ex=expire) 