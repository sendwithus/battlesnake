import logging
import json

import requests

import settings.slack

# Default Log Levels
# CRITICAL        50
# ERROR           40
# WARNING         30
# INFO            20
LOG_LEVEL_SLACK = 15
# DEBUG           10
# NOTSET          0


def install_slack_logger():
    logging.addLevelName(LOG_LEVEL_SLACK, 'SLACK')

    def log_func(self, message, *args, **kwargs):
        if self.isEnabledFor(LOG_LEVEL_SLACK):
            self._log(LOG_LEVEL_SLACK, message, args, **kwargs)

    logging.Logger.slack = log_func


class SlackLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == LOG_LEVEL_SLACK


class SlackLogHandler(logging.Handler):

    def emit(self, record):
        if settings.slack.SLACK_WEBHOOK_URL:
            try:
                headers = {
                    'content-type': 'application/json',
                }
                payload = {
                    'text': self.format(record),
                    'username': 'logger.slack',
                    'icon_emoji': ':snake:',
                    'channel': '#general'
                }

                requests.post(
                    settings.slack.SLACK_WEBHOOK_URL,
                    data=json.dumps(payload),
                    headers=headers
                )
            except:
                self.handleError(record)
