from pymongo import MongoReplicaSetClient, MongoClient

import settings.mongo

__mongo = None


def __init_connection():
    url = settings.mongo.MONGODB_URL

    if settings.mongo.MONGODB_REPLICA_SET:
        client = MongoReplicaSetClient(url, replicaSet=settings.mongo.MONGODB_REPLICA_SET)
    else:
        client = MongoClient(url)

    return client[settings.mongo.MONGODB_DATABASE]


def get_mongodb():
    global __mongo

    if __mongo is None:
        __mongo = __init_connection()

    return __mongo
