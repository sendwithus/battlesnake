import os
from pymongo import MongoReplicaSetClient, MongoClient

# Compose (MongoHQ)
MONGODB_DATABASE = 'battlesnake'

__mongo = None


def __init_connection():
    # comma-separated list of host[:port]
    hosts = os.environ.get('MONGODB_HOSTS', 'localhost')
    replica_set = os.environ.get('MONGODB_REPLICA_SET')
    username = os.environ.get('MONGODB_USERNAME')
    password = os.environ.get('MONGODB_PASSWORD')

    if username and password:
        url = 'mongodb://{username}:{password}@{hosts}/{db}'.format(
            hosts=hosts,
            username=username,
            password=password,
            db=MONGODB_DATABASE,
        )
        client = MongoReplicaSetClient(url, replicaSet=replica_set)
    else:
        client = MongoClient(hosts)

    return client[MONGODB_DATABASE]


def get_mongodb():
    global __mongo

    if __mongo is None:
        __mongo = __init_connection()

    return __mongo
