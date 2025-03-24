from pickle import dumps as pickle_dumps, loads as pickle_loads
from typing import Optional

from redis.asyncio import Redis

from ..core.config import settings


class AsyncRedis:
    redis_client: Redis = None

    @classmethod
    async def init(cls) -> Redis:
        try:
            cls.redis_client = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                # db=settings.REDIS_DB,
                username=None,
                password=None,
            )
        except Exception as e:
            raise e

        return await cls.redis_client

    @classmethod
    async def close(cls):
        if cls.redis_client is not None:
            return await cls.redis_client.aclose()

    async def save(
        self,
        key: str,
        value,
        expire: int = 0,
    ):
        return await self.redis_client.set(
            name=key, value=pickle_dumps(value), ex=expire
        )

    async def get(
        self,
        key: str,
    ):
        return pickle_loads(await self.redis_client.get(key))

    async def exists(
        self,
        key: str,
    ):
        return bool(await self.redis_client.exists(key))

    async def exists_many(
        self,
        keys: list[str],
    ):
        return await self.redis_client.exists(*keys)


class RedisDependency:
    redis: Optional[AsyncRedis] = None

    async def init(self):
        if self.redis is None:
            redis_client = AsyncRedis()
            await redis_client.init()
            self.redis = redis_client

    async def __call__(self) -> AsyncRedis:
        if self.redis is None:
            await self.init()
        return self.redis


async def get_redis() -> AsyncRedis:
    return await AsyncRedis().init()
