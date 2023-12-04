"""
Logging config
"""
import logging


def get_logger(name, level):
    logger = logging.getLogger(name)
    if level == 'INFO':
        logger.setLevel(logging.INFO)
    elif level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif level == 'WARNING':
        logger.setLevel(logging.WARNING)
    elif level == 'ERROR':
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.DEBUG)

    for handlers in get_handlers(get_formatter()):
        logger.addHandler(handlers)

    return logger


def get_formatter():
    return logging.Formatter(
        '%(levelname)s | ' +
        '%(asctime)s | ' +
        '%(process)d:%(thread)d | ' +
        '%(filename)s | ' +
        '%(funcName)s | ' +
        '%(lineno)d | ' +
        '%(message)s'
    )


def get_handlers(formatter):
    handlers = []
    handlers.append(get_stream_handler(formatter))

    return handlers


def get_stream_handler(formatter):
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    return stream_handler
