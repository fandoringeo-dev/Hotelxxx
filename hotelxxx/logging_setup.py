# logging_setup.py
import os
import sys

from loguru import logger


def setup_logging():
    env = os.getenv("APP_ENV", "dev")  # dev или prod
    level = os.getenv("LOG_LEVEL", "INFO")

    logger.remove()

    if env == "prod":
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
