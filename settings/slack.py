from os import environ

SLACK_WEBHOOK_URL = environ.get('SLACK_WEBHOOK_URL', None)
