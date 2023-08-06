import logging
from .extensions import Formatter


class ColorizeLogger(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        formatter = Formatter.get_formatter(log_level=record.levelno)

        if record.args:
            record.msg = Formatter.format_arguments(
                message=record.msg, arguments=record.args)
            record.args = None

        return formatter.format(record)
