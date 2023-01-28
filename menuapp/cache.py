import redis
import json

def start():
    global redis_client
    redis_client = redis.Redis(
        host='redis',
        port='6379',
        decode_responses=True,
    )

def get_cache(url):
    value = redis_client.get(url)
    return json.loads(value) if value else value

def set_cache(url, value):
    redis_client.set(url, json.dumps(value))

def delete_cache(url):
    keys = redis_client.keys(f'{url}*')
    if keys:
        redis_client.delete(*keys)