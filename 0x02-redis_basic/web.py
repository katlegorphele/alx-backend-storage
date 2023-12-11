#!/usr/bin/env python3
""" Web Page Cache """
import redis
from functools import wraps
from typing import Callable
import time

storage = redis.Redis()

# create a set cache decorator that takes no arguments


def set_cache(func: Callable) -> Callable:
    """Decorator to store results of function in redis"""

    @wraps(func)
    def wrapper(url):
        """Wrapper function"""
        key = f"visited:{url}"
        cached = storage.get(key)
        if cached:
            return cached.decode("utf-8")
        count = "count:{}".format(url)
        page = func(url)
        storage.incr(count)
        storage.set(key, page)
        storage.expire(key, 10)
        return page

    return wrapper


@set_cache
def get_page(url: str) -> str:
    """Get the HTML content of a particular URL and returns it."""
    from requests import get

    return get(url).text
