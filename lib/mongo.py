import os
from pymongo import MongoClient

__mongo = None


def get_mongodb():
    global __mongo

    if __mongo is None:
        __mongo = MongoClient(os.environ.get('MONGOLAB_URI', 'localhost'))

    return __mongo['battlesnake']
