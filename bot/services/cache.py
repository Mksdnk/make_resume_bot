import asyncio
import redis.asyncio as redis
from bot.config_reader import config



class CacheService:
    def __init__(self):
        self.redis_db = redis.from_url(config.REDIS_URL.unicode_string(), decode_responses=True, socket_connect_timeout=5, socket_keepalive=True)

    async def save_user_data(self, user_id: int, data: dict):
        await self.redis_db.hsetex(f'user:{user_id}', mapping=data, ex=3600)

    async def get_user_data(self, user_id: int):
        return await self.redis_db.hgetall(f'user:{user_id}')
    
    async def save_task_id(self, user_id: int, task_id: str):
        await self.redis_db.setex(f'task:{user_id}', 3600, task_id)

    async def get_task_id(self, user_id: int):
        return await self.redis_db.get(f'task:{user_id}')
    
    async def close(self):
        await self.redis_db.close()
cache_service = CacheService()
