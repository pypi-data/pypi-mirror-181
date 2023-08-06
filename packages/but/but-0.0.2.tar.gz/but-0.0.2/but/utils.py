from functools import cache
import logging


@cache
def init_logging():
    logging.basicConfig(format='%(levelname)s | %(name)s | %(message)s')


def init_log(a: str):
    init_logging()

    log = logging.getLogger(a)
    log.setLevel(logging.DEBUG)

    return log
