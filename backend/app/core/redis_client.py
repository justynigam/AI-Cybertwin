"""
Redis Connection Pool manager for CyberTwin AI Backend.
"""
import os
import redis
import logging

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

_pool: redis.ConnectionPool | None = None


def get_redis_pool() -> redis.ConnectionPool:
    """Returns singleton Redis connection pool."""
    global _pool
    if _pool is None:
        _pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)
    return _pool


def get_redis_client() -> redis.Redis:
    """Returns a Redis client instance attached to the connection pool."""
    return redis.Redis(connection_pool=get_redis_pool())
