import logging
import logging.config

from lib.log.config import LOGGING_CONFIG
from lib.log.slack import install_slack_logger


__configured = False


def get_logger(module_name):
    global __configured

    if not __configured:
        install_slack_logger()
        logging.config.dictConfig(LOGGING_CONFIG)

        __configured = True

    return logging.getLogger(module_name)
