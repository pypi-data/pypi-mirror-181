import logging
from dataclasses import dataclass


@dataclass
class Colour:
    BLUE: str = "\x1b[1;34m"
    PURPLE: str = "\x1b[1;35m"
    GREY: str = "\x1b[38;21m"
    GREEN: str = "\x1b[1;32m"
    YELLOW: str = "\x1b[33;21m"
    RED: str = "\x1b[31;21m"
    BOLD_RED: str = "\x1b[31;1m"
    DEFAULT: str = "\x1b[0m"
    DT: str = "\x1b[30;1m"


@dataclass
class Formatter:
    DT_FORMAT: str = '%Y-%m-%d %H:%M:%S %p'

    FORMATTED = dict()
    FORMATTED[logging.DEBUG] = logging.Formatter(
        fmt=f'{Colour.DT}%(asctime)s{Colour.DEFAULT} {Colour.GREY}%(levelname)-8s{Colour.DEFAULT} {Colour.PURPLE}%(name)s{Colour.DEFAULT} %(message)s',
        datefmt=DT_FORMAT)
    FORMATTED[logging.INFO] = logging.Formatter(
        fmt=f'{Colour.DT}%(asctime)s{Colour.DEFAULT} {Colour.GREEN}%(levelname)-8s{Colour.DEFAULT} {Colour.PURPLE}%(name)s{Colour.DEFAULT} %(message)s',
        datefmt=DT_FORMAT)
    FORMATTED[logging.WARNING] = logging.Formatter(
        fmt=f'{Colour.DT}%(asctime)s{Colour.DEFAULT} {Colour.YELLOW}%(levelname)-8s{Colour.DEFAULT} {Colour.PURPLE}%(name)s{Colour.DEFAULT} %(message)s',
        datefmt=DT_FORMAT)
    FORMATTED[logging.ERROR] = logging.Formatter(
        fmt=f'{Colour.DT}%(asctime)s{Colour.DEFAULT} {Colour.RED}%(levelname)-8s{Colour.DEFAULT} {Colour.PURPLE}%(name)s{Colour.DEFAULT} %(message)s',
        datefmt=DT_FORMAT)
    FORMATTED[logging.CRITICAL] = logging.Formatter(
        fmt=f'{Colour.DT}%(asctime)s{Colour.DEFAULT} {Colour.BOLD_RED}%(levelname)-8s{Colour.DEFAULT} {Colour.PURPLE}%(name)s{Colour.DEFAULT} %(message)s',
        datefmt=DT_FORMAT)

    @staticmethod
    def format_arguments(message: str, arguments: tuple) -> str:
        """Formats the arguments with 'agrs' color.

        Args:
            message (str): Debug message
            arguments (tuple): Debug arguments

        Returns:
            str: Formatted message string
        """
        parameter_count = message.count("{}")
        argument_count = len(arguments)

        if parameter_count < argument_count:
            difference = argument_count - parameter_count
            additional_param = ", ".join(["{}" for _ in range(difference)])

            spacer = f"{Colour.BOLD_RED}|{Colour.DEFAULT} argument:"
            message = f"{message} {spacer} {additional_param}"

        args = (f"{Colour.BLUE}{arg}{Colour.DEFAULT}" for arg in arguments)

        return message.format(*args)

    @staticmethod
    def get_formatter(log_level: int) -> logging.Formatter:
        return Formatter.FORMATTED.get(log_level, logging.INFO)
