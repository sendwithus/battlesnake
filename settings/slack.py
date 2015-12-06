from os import environ

SLACK_HOOK_URL = environ.get('SLACK_HOOK_URL', None)
