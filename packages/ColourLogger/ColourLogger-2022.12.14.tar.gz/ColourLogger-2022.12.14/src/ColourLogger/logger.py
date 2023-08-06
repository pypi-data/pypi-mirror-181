"""
Simples use:

import logging

from ColourLogger import logger

log = logger.build(LogLevel.DEBUG)

log.debug("This is a {} message with argument", "debug")
"""

import logging
import sys

from .colorize import ColorizeLogger


def build(log_level: int = logging.INFO) -> logging.Logger:
    """Return a colorized loggin object.

    Args:
        log_level (int, optional): Loggin level. Defaults to LogLevel.INFO.

    Returns:
        logging.Logger: Logging object
    """
    log = logging.getLogger(__name__)
    log.setLevel(log_level)

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(ColorizeLogger())

    log.addHandler(console_handler)

    return log
