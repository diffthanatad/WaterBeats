import redis


class DataBuffer:
    def __init__(self, host="localhost", port=6379, db=0):
        self._redis = None
        self._host = host
        self._port = port
        self._db = db

    def get(self, key):
        return self._get_redis().get(key)

    def set(self, key, value):
        self._get_redis().set(key, value)

    def _get_redis(self):
        if self._redis is None:
            self._redis = redis.Redis(host=self._host, port=self._port, db=self._db)
        return self._redis
