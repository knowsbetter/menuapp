import json

import redis


def start():
    global redis_client
    redis_client = redis.Redis(
        #  host='127.0.0.1',  # set host for your local machine
        host='redis',  #  Docker-compose redis host
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
