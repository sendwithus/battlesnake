import os

from redis import StrictRedis


__redis = None


def __init_connection():
    host = os.environ.get('REDIS_HOST', 'localhost')
    db = int(os.environ.get('REDIS_DB', '0'))

    return StrictRedis(host=host, db=db)


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
