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

    def hset_sorted(self, k, field_and_values, score, z_key, member, set_key=None):
        '''
        Insert a new record into the sorted set and add the sorted set keys to a set.
        Parameters:
            k: key of the hash
            field_and_values: dict of field and values to be inserted into the hash
            score: score of the sorted set
            z_key: key of the sorted set
            member: member of the sorted set
            set_key: key of the set (that scores the key to all the sorted sets)
        '''
        pipeline = self._get_redis().pipeline()
        pipeline.zadd(z_key, {member: score})
        for field, value in field_and_values.items():
            pipeline.hset(k, field, value)
        if set_key:
            pipeline.sadd(set_key, z_key)
        return pipeline.execute()
    
    def get_all_by_value_range(self, set_key: str, min: int, max: int):
        '''
        Get all the data indexed by the sorted sets in the set whose score is in the range [min, max]

            Parameters:
                set_key: key of the set
                min: min score
                max: max score
        '''
        r = self._get_redis()
        members = r.smembers(set_key)
        pipeline = r.pipeline()
        for m in members:
            pipeline.zrangebyscore(m, 0, max)
        keys = pipeline.execute() # List[List[bytes]
        pipeline = r.pipeline()
        del_pipeline = r.pipeline()
        for sorted_set in keys:
            if not sorted_set:
                del_pipeline.srem(set_key, sorted_set)
            for key in sorted_set:
                pipeline.hgetall(key)
        data = []
        for ele in pipeline.execute():
            data.append(ele)
        return data

    def delete_all_by_value_range(self, set_key: str, min: int, max: int):
        r = self._get_redis()
        members = r.smembers(set_key)
        print('members', members)
        pipeline = r.pipeline()
        for m in members:
            pipeline.zrangebyscore(m, 0, max)
        keys = pipeline.execute()
        for sorted_set in keys:
            print("sorted_set", sorted_set)
            for key in sorted_set:
                print("del key", key)
                pipeline.delete(key)
        for m in members:
            print("del sorted set", m, min, max)
            pipeline.zremrangebyscore(m, min, max)
        pipeline.execute()

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
