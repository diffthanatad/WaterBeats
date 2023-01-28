from typing import List
import redis


class DataBuffer:
    def __init__(self, host="localhost", port=6379, db=0):
        self._redis = None
        self._host = host
        self._port = port
        self._db = db

    def get(self, key):
        return self._get_redis().get(key)

    def hgetall(self, key):
        return self._get_redis().hgetall(key)

    def pipeline_hget(self, name, fields: List[str]):
        pipeline = self._get_redis().pipeline()
        for field in fields:
            pipeline.hget(name, field)
        return pipeline.execute()

    def hset(self, name, field_and_values: dict):
        pipeline = self._get_redis().pipeline()
        for field, value in field_and_values.items():
            pipeline.hset(name, field, value)
        pipeline.execute()

    def delete(self, key):
        num_keys_del = self._get_redis().delete(key)
        return num_keys_del

    def hset_sorted(self, k, field_and_values, score, z_key, member):
        pipeline = self._get_redis().pipeline()
        pipeline.zadd(z_key, {member: score})
        for field, value in field_and_values.items():
            pipeline.hset(k, field, value)
        return pipeline.execute()

    def pop_sorted(self, z_key, fields: List[str]):
        r = self._get_redis()
        top_member = r.zrange(z_key, -1, -1)
        if not top_member:
            return None
        top_member = top_member[0]
        pipeline = r.pipeline()
        for field in fields:
            pipeline.hget(top_member, field)
        pipeline.delete(top_member).zrem(z_key, top_member)
        ret = pipeline.execute()
        print(ret)
        return top_member, ret[: len(fields)]

    def _get_redis(self) -> redis.Redis:
        if self._redis is None:
            try:
                self._redis = redis.Redis(host=self._host, port=self._port, db=self._db)
            except redis.exceptions.ConnectionError as e:
                print("Redis connection error", e)
        return self._redis
