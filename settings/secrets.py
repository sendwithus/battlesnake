from os import environ

SESSION_KEY = environ.get('SESSION_KEY', 'lollipop')
OVERRIDE_AUTH_HEADER = environ.get('OVERRIDE_AUTH_HEADER', 'lollipop')
