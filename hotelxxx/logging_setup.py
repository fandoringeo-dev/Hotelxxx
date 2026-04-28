# logging_setup.py
import os
import sys

from django.conf import settings
from loguru import logger


def setup_logging():
    level = os.getenv("LOG_LEVEL", "INFO")

    logger.remove()

    if not settings.DEBUG:
        logger.add(
            sys.stdout,
            level=level,
            serialize=True,
            enqueue=True,
        )
    else:
        fmt = "<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>"
        logger.add(sys.stdout, level=level, format=fmt)

    return logger
