from redis import StrictRedis

import settings.redis

__redis = None


def __init_connection():
    return StrictRedis(
        host=settings.redis.REDIS_HOST,
        port=settings.redis.REDIS_PORT,
        db=settings.redis.REDIS_DB,
        password=settings.redis.REDIS_PASSWORD
    )


def get_redis():
    global __redis

    if __redis is None:
        __redis = __init_connection()

    return __redis


class Queue(object):
    def __init__(self, key):
        self.key = key

    @property
    def client(self):
        return get_redis()

    def enqueue(self, *args):
        # Push args onto the tail of the list
        return self.client.rpush(self.key, *args)

    def dequeue(self, timeout=0):
        # Remove and return the first item of the list, blocking until timeout seconds
        # or indefinitely, if timeout=0
        result = self.client.blpop(self.key, timeout=timeout)
        if result is None:
            return None
        queue, value = result
        return value

    def items(self):
        # Get all items in the list
        return self.client.lrange(self.key, 0, -1)
