"""
Code service.

Code service is a service that allows you to create a code and store it in redis. It is used for example to create a code for email confirmation.
"""  # noqa: EXE002, E501

import random
import string

from redis import asyncio as aioredis


class CodeService:
    """
    Service class for generating and managing codes using Redis.

    Attributes
    ----------
        redis (aioredis.Redis): Redis instance for code storage.
        key (str): Key prefix for Redis storage.

    Methods
    -------
        generate: Generate a random code.
        get_redis_key: Get the Redis key for a given code.
        create: Create a code and store it in Redis.
        get: Get the data associated with a code from Redis.
        delete: Delete a code and its associated data from Redis.
    """

    redis: aioredis.Redis
    key: str

    def __init__(self, redis: aioredis.Redis, key: str) -> None:
        """Initialize the CodeService."""
        self.redis = redis
        self.key = key

    @staticmethod
    def generate(number: int = 8) -> str:
        """
        Generate a random string of digits.

        Args:
        ----
            number (int): The length of the generated string. Default is 8.

        Returns:
        -------
            str: A random string of digits.
        """
        return "".join(random.choice(string.digits) for _ in range(number))  # noqa: S311

    def get_redis_key(self, code: str) -> str:
        """
        Return the Redis key for the given code.

        Args:
        ----
            code (str): The code to generate the Redis key for.

        Returns:
        -------
            str: The Redis key.
        """
        return f"{self.key}:{code}"

    async def create(
        self, data: any, code_len: int = 8, expire: int = 60 * 60,
    ) -> (str, str):
        """
        Create a code and stores it in Redis with the provided data.

        Args:
        ----
            data (any): The data to be stored along with the code.
            code_len (int, optional): The length of the generated code. Defaults to 8.
            expire (int, optional): The expiration time of the code in seconds. Defaults to 3600.

        Returns:
        -------
            Tuple[str, str]: A tuple containing the code key and the stored data.
        """  # noqa: E501
        code = self.generate(number=code_len)
        redis_key = self.get_redis_key(code)
        if await self.redis.exists(redis_key):
            await self.redis.delete(redis_key)
        await self.redis.set(redis_key, data)
        await self.redis.expire(redis_key, expire)
        return redis_key.split(":")[1], await self.redis.get(redis_key)

    async def get(self, code: str) -> str:
        """
        Retrieves the value associated with the given code from Redis.

        Args:
        ----
            code (str): The code to retrieve the value for.

        Returns:
        -------
            str: The value associated with the code.
        """  # noqa: D401
        return await self.redis.get(self.get_redis_key(code))

    async def delete(self, code: str) -> bool:
        """
        Delete a code from the Redis cache.

        Args:
        ----
            code (str): The code to be deleted.

        Returns:
        -------
            bool: True if the code was successfully deleted, False otherwise.
        """
        return await self.redis.delete(self.get_redis_key(code))
