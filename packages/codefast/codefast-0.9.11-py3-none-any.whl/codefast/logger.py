# coding:utf-8
import logging
from logging.handlers import RotatingFileHandler


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    bold_yellow = "\x1b[33;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s %(module)s %(filename)s:%(lineno)d %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: bold_yellow + format + reset,
        logging.ERROR: bold_red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


log_file = '/tmp/cf.log'

my_handler = RotatingFileHandler(log_file, mode='a', maxBytes=100*1024*1024,
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(CustomFormatter())
my_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(CustomFormatter())
stream_handler.setLevel(logging.INFO)

logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

logger.addHandler(my_handler)
logger.addHandler(stream_handler)


def _log_print(msg: str, *args, **kwargs) -> str:
    if args:
        msg = f"{msg}, args: {args}"
    if kwargs:
        msg = f"{msg}, kwargs: {kwargs}"
    return msg


def info(msg: str, *args, **kwargs):
    msg = _log_print(msg, *args, **kwargs)
    logger.info(msg)


def warning(msg: str, *args, **kwargs):
    msg = _log_print(msg, *args, **kwargs)
    logger.warning(msg)


def error(msg: str, *args, **kwargs):
    msg = _log_print(msg, *args, **kwargs)
    logger.error(msg)


class Logger(object):
    def info(self, msg: str):
        info(msg)

    def warning(self, msg: str):
        warning(msg)

    def error(self, msg: str):
        error(msg)
