import logging
import logging.config

from lib.log.config import LOGGING_CONFIG
from lib.log.slack import install_slack_logger


g_configured = False


def get_logger(module_name):
    global g_configured

    if not g_configured:
        install_slack_logger()
        logging.config.dictConfig(LOGGING_CONFIG)

    return logging.getLogger(module_name)
