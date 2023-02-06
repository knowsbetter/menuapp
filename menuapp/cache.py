import json

import redis.asyncio as redis

from . import config

redis_client: redis.Redis = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)


async def stop():
    await redis_client.flushall()
    await redis_client.close()


async def get_cache(url):
    """Returns cached value or None for given url"""
    value = await redis_client.get(url)
    return json.loads(value) if value else value


async def set_cache(url, value):
    """Sets cache value for given url"""
    await redis_client.set(url, json.dumps(value))


async def delete_cache(url):
    """Deletes cache for given url"""
    keys = await redis_client.keys(f"{url}*")
    if keys:
        await redis_client.delete(*keys)
