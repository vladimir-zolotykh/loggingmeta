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
    logger.propagate = True
    if not logger.handlers:
        handler = (
            logging.FileHandler(filename, mode=filemode)
            if filename is not None
            else logging.StreamHandler()
        )
        formatter = logging.Formatter(logformat)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


LOGFILENAME = f".{os.path.splitext(os.path.basename(__file__))[0]}.log"


class LoggingMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):

        filename = kwargs.get("filename") if "filename" in kwargs else LOGFILENAME
        logger = setup_class_logger(name=name, filename=filename)
        for attr, obj in namespace.items():
            if callable(obj) and not attr.startswith("__"):
                namespace[attr] = mcs._wrap_method(obj, logger)
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

    @staticmethod
    def _wrap_method(method, logger):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            logger.info(f"{method.__name__!r} is called with {args[1:]}, {kwargs}")
            res = method(*args, **kwargs)
            logger.info(f"{method.__name__!r} returns {res}")
            return res

        return wrapper


class ID3(metaclass=LoggingMeta, filename=LOGFILENAME):
    def sum(self, x, y) -> int:
        return x + y

    def greeting(self, name="Vladimir") -> str:
        msg: str = f"Hello, {name}!"
        print(msg)
        return msg


def test_sum(caplog):
    id3 = ID3()
    id3.sum(3, 4)
    assert any(
        "'sum' is called with (3, 4)" in record.message for record in caplog.records
    )
    assert any("'sum' returns 7" in record.message for record in caplog.records)


if __name__ == "__main__":
    id3 = ID3()
    id3.sum(3, 4)
    id3.greeting("Schscraah")
