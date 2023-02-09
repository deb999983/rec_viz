import json
import redis
from django.conf import settings


redis_conn = redis.Redis(charset="utf-8", decode_responses=True, **settings.QUEUE_CONN_PARAMS)


def enqueue(data):
	redis_conn.rpush("write_queue", json.dumps(data))
	return data


def dequeue():
    message = redis_conn.lpop("write_queue")
    if not message:
        return
    return json.loads(message)
