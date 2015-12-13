from os import environ

REDIS_HOST = environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(environ.get('REDIS_PORT', '6379'))
REDIS_DB = int(environ.get('REDIS_DB', '0'))
