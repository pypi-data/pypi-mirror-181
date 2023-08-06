import datetime

import orjson as json
import redis


class BaseCache:
    @classmethod
    def get_class(cls, key):
        for _class in cls.__subclasses__():
            if _class.__name__ == key:
                return _class
        return DumpCache


class KeyDBCache(BaseCache):
    CONNECT = None

    def __init__(self, *args, dsn, cache_period):
        if not self.CONNECT:
            self.CONNECT = redis.Redis.from_url(dsn)
        self.cache_period = cache_period

    def get(self, key, default=None):
        return self[key] or default

    def __getitem__(self, key):
        value = self.CONNECT.get(key)
        if value:
            return json.loads(value)

    def __setitem__(self, key, value):
        self.CONNECT.setex(key, self.cache_period, json.dumps(value))


class DumpCache(BaseCache):
    CACHE = {}

    def __init__(self, *args, dsn, cache_period):
        self.cache_period = cache_period

    def get(self, *args, **kwargs):
        return self.CACHE.get(*args, **kwargs)

    def __getitem__(self, key):
        cached = self.CACHE.get(key)
        if cached and cached["time"] > datetime.datetime.now():
            return self.CACHE[key]["data"]

    def __setitem__(self, key, value):
        self.CACHE[key] = {
            "data": value,
            "time": datetime.datetime.now()
            + datetime.timedelta(seconds=self.cache_period),
        }
