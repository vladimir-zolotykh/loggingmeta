#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import logging
import functools
import os


def setup_class_logger(
    name: str,
    log_level: int = logging.INFO,
    filename: str = None,
    logformat: str = "%(levelname)s: %(name)s %(message)s",
    filemode: str = "w",
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    if not logger.handlers:
        handler = (
            logging.FileHandler(filename)
            if filename is not None
            else logging.StreamHandler()
        )
        formatter = logging.Formatter(logformat)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


class LoggingMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):

        if 'filename' in kwargs:
        filename = kwargs.get(
            "filename", f".{os.path.splitext(os.path.basename(__file__))[0]}.log"
        )
        logger = setup_class_logger(name, filename)
        for attr, obj in namespace.items():
            if callable(obj) and not attr.startswith("__"):
                namespace[attr] = mcs._wrap_method(obj, logger)
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

    @staticmethod
    def _wrap_method(method, logger):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            logger.info(f"{method.__qualname__} is called with {args}, {kwargs}")
            res = method(*args, **kwargs)
            logger.info(f"returns {res}")
            return res

        return wrapper


class ID3(metaclass=LoggingMeta, filename=None):
    pass


if __name__ == "__main__":
    id3 = ID3()
