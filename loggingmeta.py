#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import logging
import functools


def setup_class_logger(
    name: str,
    log_level: int = logging.INFO,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger


class LoggingMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        print(f"{mcs = }")
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

    @staticmethod
    def _wrap_method(method, logger):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            pass

        return wrapper


class ID3(metaclass=LoggingMeta):
    pass


if __name__ == "__main__":
    id3 = ID3()
