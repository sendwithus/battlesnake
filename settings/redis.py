from os import environ
from urlparse import urlparse


# Try for Heroku Redis first
if environ.get('REDIS_URL'):
    parsed_url = urlparse(environ.get('REDIS_URL'))
    REDIS_HOST = '%s:%s@%s' % (parsed_url.username, parsed_url.password, parsed_url.hostname)
    REDIS_PORT = parsed_url.port
    REDIS_DB = '0'

# Try local config
else:
    REDIS_HOST = environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(environ.get('REDIS_PORT', '6379'))
    REDIS_DB = int(environ.get('REDIS_DB', '0'))
