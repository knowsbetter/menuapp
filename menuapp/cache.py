import json

import redis

from . import config


def start():
    global redis_client
    redis_client = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        decode_responses=True,
    )

def get_cache(url):
    """Returns cached value or None for given url"""
    value = redis_client.get(url)
    return json.loads(value) if value else value

def set_cache(url, value):
    """Sets cache value for given url"""
    redis_client.set(url, json.dumps(value))

def delete_cache(url):
    """Deletes cache for given url"""
    keys = redis_client.keys(f'{url}*')
    if keys:
        redis_client.delete(*keys)
