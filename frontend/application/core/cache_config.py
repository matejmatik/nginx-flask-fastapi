from flask import Flask
from flask_caching import Cache

RedisCache = Cache(
    app=Flask(__name__),
    config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_URL": "redis://redis:6379",
        "CACHE_REDIS_DB": 0,
        "CACHE_THRESHOLD": 1000,
    },
)
