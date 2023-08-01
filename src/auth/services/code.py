import random
import string

from redis import asyncio as aioredis


class CodeService:
    redis: aioredis.Redis
    key: str

    def __init__(self, redis: aioredis.Redis, key: str):
        self.redis = redis
        self.key = key

    @staticmethod
    def generate(number: int = 8):
        """
        Generate code
        :param number:
        :return:
        """
        return "".join(random.choice(string.digits) for _ in range(number))

    def get_redis_key(self, code: str):
        return f"{self.key}:{code}"

    async def create(self, data: any, code_len: int = 8, expire: int = 60 * 60):
        """
        Create code
        :param code_len:
        :param data:
        :param expire:
        :return:
        """
        code = self.generate(number=code_len)
        redis_key = self.get_redis_key(code)
        if await self.redis.exists(redis_key):
            await self.redis.delete(redis_key)
        await self.redis.set(redis_key, data)
        await self.redis.expire(redis_key, expire)
        return redis_key.split(":")[1], await self.redis.get(redis_key)

    async def get(self, code: str):
        return await self.redis.get(self.get_redis_key(code))

    async def delete(self, code: str):
        return await self.redis.delete(self.get_redis_key(code))
