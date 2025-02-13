import time

class Cache:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Cache, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, default_ttl=5):
        if not hasattr(self, 'initialized'):
            self.default_ttl = default_ttl
            self.cache = {}
            self.initialized = True

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def set(cls, key, value, ttl=None):
        """ Set a value in the cache """
        cls.instance().set_instance(key, value, ttl)

    @classmethod
    def set_result(cls, key, func, *args, **kwargs):
        """ Sets result of a function in the cache and returns the result """
        result = func(*args, **kwargs)
        cls.set(key, result)
        return result

    @classmethod
    def get(cls, key):
        return cls.instance().get_instance(key)

    @classmethod
    def delete(cls, key):
        cls.instance().delete_instance(key)

    @classmethod
    def clear(cls):
        cls.instance().clear_instance()

    def set_instance(self, key, value, ttl=None):
        if ttl is None:
            ttl = self.default_ttl
        expire_at = time.time() + ttl
        self.cache[key] = (value, expire_at)

    def get_instance(self, key):
        if key in self.cache:
            value, expire_at = self.cache[key]
            if time.time() < expire_at:
                return value
            else:
                del self.cache[key]
        return None

    def delete_instance(self, key):
        if key in self.cache:
            del self.cache[key]

    def clear_instance(self):
        self.cache.clear()