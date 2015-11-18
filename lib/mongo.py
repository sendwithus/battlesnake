import os
from pymongo import MongoReplicaSetClient, MongoClient

# Compose (MongoHQ)
MONGODB_DATABASE = 'battlesnake'

__mongo = None


def __init_connection():
    username = os.environ.get('MONGODB_USERNAME')
    password = os.environ.get('MONGODB_PASSWORD')

    if username and password:
        url = 'mongodb://%s:%s@candidate.48.mongolayer.com:10146,candidate.11.mongolayer.com:10639/%s' % (
            username, password, MONGODB_DATABASE
        )
        client = MongoReplicaSetClient(url, replicaSet='set-54def1ba0a1d8017550006f3')
    else:
        client = MongoClient('localhost')

    return client[MONGODB_DATABASE]


def get_mongodb():
    global __mongo

    if __mongo is None:
        __mongo = __init_connection()

    return __mongo
