import logging
import logging.config
import os
import re
from datetime import datetime
from typing import List

from src import settings

REMOVE_ANSI_RE = r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"  # from https://stackoverflow.com/a/14693789
REGISTERED_LOGGERS: List[logging.Logger] = []

LOG_FILE_NAME = (
    f"log_{datetime.now().strftime(settings.Logging().get_file_timestamp())}.log"
)
LOG_FILE_PATH = os.path.join(settings.Logging().get_path(), LOG_FILE_NAME)


class ANSIColors:
    DEFAULT = "\033[0;39m"
    RESET = "\x1b[0m"

    # Foreground colors
    RED = "\033[0;31m"
    YELLOW = "\033[1;33m"
    GREEN = "\033[0;32m"
    CYAN = "\033[1;36m"
    BLUE = "\033[1;34m"
    PURPLE = "\033[0;35m"

    # Effects
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"


class ColoredFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: ANSIColors.BLUE
        + ANSIColors.FAINT
        + settings.Logging().get_format()
        + ANSIColors.RESET,
        logging.INFO: ANSIColors.DEFAULT
        + settings.Logging().get_format()
        + ANSIColors.RESET,
        logging.WARNING: ANSIColors.YELLOW
        + settings.Logging().get_format()
        + ANSIColors.RESET,
        logging.ERROR: ANSIColors.RED
        + ANSIColors.BOLD
        + settings.Logging().get_format()
        + ANSIColors.RESET,
        logging.CRITICAL: ANSIColors.RED
        + ANSIColors.BOLD
        + ANSIColors.NEGATIVE
        + ANSIColors.BLINK
        + settings.Logging().get_format()
        + ANSIColors.RESET,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno, settings.Logging().get_format())
        return logging.Formatter(log_fmt).format(record)


class FileLoggerFormatter(logging.Formatter):
    regex = re.compile(REMOVE_ANSI_RE)

    def format(self, record: logging.LogRecord) -> str:
        entry = super().format(record)
        return self.regex.sub("", entry)


def setup_logging() -> None:

    # Check if the log directory exists
    if not os.path.exists(settings.Logging().get_path()):
        os.makedirs(settings.Logging().get_path())

    # Configure the logger
    logging.config.dictConfig(get_logger_config())


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger not in REGISTERED_LOGGERS:
        REGISTERED_LOGGERS.append(logger)
    return logger


def update_log_level(level: int) -> None:
    for logger in REGISTERED_LOGGERS:
        logger.setLevel(level)


def get_logger_config() -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored": {
                "()": ColoredFormatter,
            },
            "file": {
                "()": FileLoggerFormatter,
                "format": settings.Logging().get_format(),
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "colored",
                "level": settings.Logging().get_level(),
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "file",
                "level": settings.Logging().get_level(),
                "filename": LOG_FILE_PATH,
                "maxBytes": settings.Logging().get_max_size(),
                "backupCount": settings.Logging().get_max_backups(),
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": settings.Logging().get_level(),
        },
    }
