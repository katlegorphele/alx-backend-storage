#!/usr/bin/env python3
""" python redis practice scripts """
import redis
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Count the number of times a method is called
    """
    key = method.__qualname__  # Generate a unique key

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Callable:
        """ Wrapper function
        """
        self._redis.incr(key)  # Increment the key
        return method(self, *args, **kwargs)  # Call the method
    return wrapper


def call_history(method: Callable) -> Callable:
    """ method call history decorator

    Args:
        method (Callable): function being decoratd

    Returns:
        Callable: new wrapper function
    """
    @wraps(method)  # to get all original function docs and props
    def wrapper(self, *args, **kwargs) -> str:
        """ Wrapper function

        Returns:
            Callable: decorated function
        """
        input_args = str(args)
        key = method.__qualname__
        self._redis.rpush(key + ":inputs", input_args)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(key + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """ Display the history of calls of a particular function
    """
    r = redis.Redis()
    key = fn.__qualname__
    count = r.get(key).decode("utf-8")
    inputs = r.lrange(f"{key}:inputs", 0, -1)
    outputs = r.lrange(f"{key}:outputs", 0, -1)
    print("{} was called {} times:".format(key, count))
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(key, i.decode("utf-8"),
                                     o.decode("utf-8")))


class Cache:
    """ Cache Storage class
    """

    def __init__(self) -> None:
        self._redis: redis.Redis = redis.Redis()  # Redis client instance
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key: str = str(uuid4())  # Generate a unique key
        self._redis.set(key, data)  # Store the data in Redis
        return key  # Return the key for later retrieval

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> Union[str, bytes, int, float]:
        """ Get a value from Redis and convert it to the desired format
        """
        # get the data from redis
        data = self._redis.get(key)
        # if a function was passed, apply it to the data
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Convert data to str
        """
        result = self._redis.get(key)
        return str(result.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ Convert data to int
        """
        result = self._redis.get(key)
        return int(result.decode("utf-8"))
