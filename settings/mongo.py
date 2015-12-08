from os import environ

MONGODB_DATABASE = environ.get('MONGODB_DATABASE', 'battlesnake')
MONGODB_URL = environ.get('MONGODB_URL', 'mongodb://localhost:27017/{}'.format(MONGODB_DATABASE))
MONGODB_REPLICA_SET = environ.get('MONGODB_REPLICA_SET', None)
