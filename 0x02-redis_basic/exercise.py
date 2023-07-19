#!/usr/bin/env python3
"""Redis module"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Count how many times methods of the Cache class are called"""

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwds)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a particular function"""

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper function"""
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        output = method(self, *args, **kwds)
        self._redis.rpush(method.__qualname__ + ":outputs", str(output))
        return output

    return wrapper


class Cache:
    """Cache class"""
    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) ->\
            Union[str, bytes, int, float, None]:
        """Get data from redis"""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Get data from redis as string"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Get data from redis as integer"""
        return self.get(key, int)


def replay(val: Cache):
    """display history of all calls made on a particular class"""
    clsName = val.__qualname__
    print(f"""{clsName} was called {
            val.__self__.get(clsName).decode("utf-8")} times:""")
    inputs = val.__self__._redis.lrange(f"{clsName}:inputs", 0, -1)
    outputs = val.__self__._redis.lrange(f"{clsName}:outputs", 0, -1)
    zipped = zip(inputs, outputs)
    for i, o in zipped:
        print(f"""{clsName}(*{i.decode("utf-8")}) -> {o.decode("utf-8")}""")
