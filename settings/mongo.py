from os import environ

MONGODB_URL = environ.get('MONGODB_HOST', 'mongodb://localhost:27017/battlesnake')
MONGODB_DATABASE = environ.get('MONGODB_DATABASE', 'battlesnake')
MONGODB_REPLICA_SET = environ.get('MONGODB_REPLICA_SET', None)
