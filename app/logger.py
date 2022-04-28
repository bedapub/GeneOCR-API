import logging
import os
import sys

import loguru
from fastapi import FastAPI
from loguru import logger

logger: loguru.logger = logger
logger.remove()


def configure_logger(app: FastAPI, logger_instance: loguru.logger):
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    if log_level in ['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL']:
        log_level = logging.getLevelName(log_level)

    if app.debug:
        log_level = logging.DEBUG

    logger_instance.add(
        sys.stdout,
        colorize=True,
        level=logging.getLevelName(log_level),
        format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>"
    )
