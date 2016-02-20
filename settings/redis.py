from os import environ
from urlparse import urlparse


# Try for Heroku Redis first
if environ.get('REDISCLOUD_URL'):
    parsed_url = urlparse(environ.get('REDISCLOUD_URL'))
    REDIS_HOST = parsed_url.hostname
    REDIS_PORT = parsed_url.port
    REDIS_PASSWORD = parsed_url.password
    REDIS_DB = '0'

# Try local config
else:
    REDIS_HOST = environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(environ.get('REDIS_PORT', '6379'))
    REDIS_PASSWORD = environ.get('REDIS_PASSWORD')
    REDIS_DB = int(environ.get('REDIS_DB', '0'))
