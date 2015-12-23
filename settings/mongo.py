from os import environ

# Try MONGOHQ first...
if environ.get('MONGOHQ_URL'):
    MONGODB_URL = environ.get('MONGOHQ_URL')
    MONGODB_DATABASE = MONGODB_URL.split('/')[-1]

# Try local config
else:
    MONGODB_DATABASE = environ.get('MONGODB_DATABASE', 'battlesnake')
    MONGODB_URL = environ.get(
        'MONGODB_URL',
        'mongodb://localhost:27017/{}'.format(MONGODB_DATABASE)
    )

# This probably will never be used.
MONGODB_REPLICA_SET = environ.get('MONGODB_REPLICA_SET', None)
