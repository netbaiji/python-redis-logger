"""
redis_logger - a persistent redis logging handler for python

>>> from redis_logger import RedisLogger
>>> l = RedisLogger('test')
>>> l.info("I like pie!")
>>> l.error("Oh snap")

On errors, if exc_info is True, a printed traceback will be included.
"""

__author__ = 'Teodor Pripoae <toni@netbaiji.com>'
__version__ = (0, 0, 1)

from redis_logger import RedisLogger
