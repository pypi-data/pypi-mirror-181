import redis
import datetime


class LzRedisKey(object):

    def key_rename(self, old, new) -> bool: ...

    # ==========================================================
    def key_reset_expire_time_s(self, key, time) -> bool: ...

    def key_reset_expire_time_ms(self, key, time) -> bool: ...

    def key_reset_expire_timestamp(self, key, timestamp) -> bool: ...

    # ==========================================================
    def key_num_value_increment(self, key) -> bool: ...

    def key_num_value_decrease(self, key) -> bool: ...

    def key_num_value_increment_by(self, key, num: int) -> bool: ...

    def key_num_value_decrease_by(self, key, num: int) -> bool: ...

    # ==========================================================
    def key_delete(self, key) -> bool: ...

    def key_move_to_db(self, key, db_num: int) -> bool: ...

    # ==========================================================
    def keys(self, reg: str = '*') -> list: ...

    def key_random(self) -> str: ...

    # ==========================================================
    def key_remain_time_s(self, key) -> int: ...

    def key_remain_time_ms(self, key) -> int: ...

    # ==========================================================
    def key_exists(self, key) -> bool: ...

    def key_type(self, key) -> str: ...


class LzRedisString(object):
    def string_set_s(self, time=None, **key_value) -> bool: ...

    def string_set_ms(self, time=None, **key_value) -> bool: ...

    # ==========================================================
    def string_append(self, key, value) -> bool: ...

    def string_getset(self, key, value) -> str: ...

    # ==========================================================
    def string_get(self, key) -> str: ...

    def string_mget(self, *keys) -> str: ...

    def string_len(self, key) -> int: ...


class LzRedisHash(object):
    def hash_set(self, key, **k_v): ...

    def hash_append(self, key, **k_v): ...

    # ==========================================================
    def hash_delete_fields(self, key, **k_v): ...

    # ==========================================================
    def hash_get(self, key, k): ...

    def hash_mget(self, key, *k): ...

    def hash_get_items(self, key): ...

    def hash_get_fields(self, key): ...

    def hash_get_values(self, key): ...

    # ==========================================================
    def hash_exists_field(self, key, k): ...

    def hash_fields_len(self, key): ...

    def hash_match_field(self, key, field_reg): ...


class LzRedisList(object):

    def list_lpush(self, key, *values): ...

    def list_rpush(self, key, *values): ...

    # ==========================================================
    def list_linsert(self, key, pos_value, value, before: bool = True): ...

    def list_lset(self, key, index, value): ...

    # ==========================================================
    def list_lpop(self, key): ...

    def list_lpop_wait_s(self, key, time=1): ...

    def list_rpop(self, key): ...

    def list_rpop_wait_s(self, key, time=1): ...

    # ==========================================================
    def list_remove_value(self, key, value, num=0, from_left=True): ...

    # [start_index, end_index], [0, -1]
    def list_trim_slice(self, key, start_index, end_index): ...

    def list_slice(self, key, start_index, end_index): ...

    def list_index_value(self, key, index): ...


class LzRedisSet(object):
    def set_add(self, key, *values): ...

    # ==========================================================
    def set_move(self, from_key, to_key, value): ...

    def set_random_pop(self, key): ...

    def set_remove(self, key, *values): ...

    # ==========================================================
    def set_len(self, key): ...

    # ==========================================================
    def set_logic_sub(self, key, *other_keys): ...

    def set_logic_sub_tokey(self, tokey, key, *other_keys): ...

    def set_logic_and(self, key, *other_keys): ...

    def set_logic_and_tokey(self, tokey, key, *other_keys): ...

    def set_logic_or(self, key, *other_keys): ...

    def set_logic_or_tokey(self, tokey, key, *other_keys): ...

    # ==========================================================
    def set_exists(self, key, value): ...

    def set_get(self, key): ...

    def set_random_get(self, key, num=1): ...


class LzRedisZSet(object):
    def zset_add(self, key, *w_v): ...

    def zset_value_increment(self, key, value, add_num): ...

    def zset_remove(self, key, *values): ...

    def zset_remove_score_range(self, key, start_score, end_score): ...

    # ==========================================================
    # [start_index, end_index]
    def zset_slice(self, key, start_index, end_index, withscore=False): ...

    # [start_score, end_score],-> (limit_offset, limit_offset+limit_count]
    def zset_slice_score(self, key, start_score=None, end_score=None,
                         start_score_no=None, end_score_no=None,
                         limit_offset=None, limit_count=None): ...

    # ==========================================================
    def zset_score_by_value(self, key, value): ...

    def zset_len(self, key): ...

    def zset_slice_score_count(self, key, min_score, max_score): ...

    def zset_slice_count(self, key, min_value, max_value): ...

    def zset_value_by_score_rank(self, key, value, reverse=False): ...


class LzRedis(LzRedisKey, LzRedisString, LzRedisHash, LzRedisList, LzRedisSet, LzRedisZSet):

    def init(self, host: str = '127.0.0.1', port: int = 6379, password: str = None, db_num: int = 0): ...


class LzRedisImp(LzRedis):
    __redis_pool: redis.ConnectionPool = None
    __redis_conn: redis.Redis = None

    def __init__(self, host: str = '127.0.0.1', port: int = 6379, password: str = None, db_num: int = 0) -> None:
        self.init(host, port, password, db_num)

    def init(self, host: str = '127.0.0.1', port: int = 6379, password: str = None, db_num: int = 0) -> None:
        # redis返回的数据解码为字符串(默认为byte)
        self.__redis_pool = redis.ConnectionPool(host=host, port=port,
                                                 password=password, db=db_num, decode_responses=True,
                                                 max_connections=10)
        self.__redis_conn = redis.Redis(connection_pool=self.__redis_pool, decode_responses=True)

    def redis_connection(self, new=False) -> redis.Redis:
        if new is True:
            return redis.Redis(connection_pool=self.__redis_pool, decode_responses=True)
        else:
            return self.__redis_conn

    # ============================================================
    def key_rename(self, old: str, new: str) -> bool:
        return self.__redis_conn.rename(old, new)

    def key_reset_expire_time_s(self, key: str, time: int) -> bool:
        return bool(self.__redis_conn.expire(key, time))

    def key_reset_expire_time_ms(self, key: str, time: int) -> bool:
        return bool(self.__redis_conn.pexpire(key, time))

    def key_reset_expire_timestamp(self, key: str, timestamp: float) -> bool:
        return bool(self.__redis_conn.expireat(key, timestamp))

    def key_reset_expire_datetime(self, key: str, arg_datetime: datetime.datetime) -> bool:
        return bool(self.__redis_conn.pexpire(key, arg_datetime.timestamp()))

    def key_num_value_increment(self, key: str) -> int:
        return self.key_num_value_increment_by(key, num=1)

    def key_num_value_decrease(self, key: str) -> int:
        return self.key_num_value_decrease_by(key, num=1)

    def key_num_value_increment_by(self, key: str, num: int) -> int:
        return self.__redis_conn.incrby(key, num)

    def key_num_value_increment_by_float(self, key: str, num: float) -> float:
        return self.__redis_conn.incrbyfloat(key, num)

    def key_num_value_decrease_by(self, key: str, num: int) -> int:
        return self.__redis_conn.decrby(key, num)

    def key_delete(self, key: str) -> bool:
        return bool(self.__redis_conn.delete(key))

    def key_move_to_db(self, key: str, db_num: int) -> bool:
        return self.__redis_conn.move(key, db_num)

    # * 表示任意多个字符, key* , *_num,
    def keys(self, reg: str = '*') -> list:
        return self.__redis_conn.keys().keys(reg)

    def key_random(self) -> str:
        return self.__redis_conn.randomkey()

    # -1 表示永久
    def key_remain_time_s(self, key: str) -> int:
        if not self.key_exists(key):
            raise Exception(f'键 {key} 不存在')

        return self.__redis_conn.ttl(key)

    # -1 表示永久
    def key_remain_time_ms(self, key: str) -> int:
        if not self.key_exists(key):
            raise Exception(f'键 {key} 不存在')

        return self.__redis_conn.pttl(key)

    def key_exists(self, key: str) -> bool:
        return bool(self.__redis_conn.exists(key))

    def key_type(self, key: str) -> str:
        res = self.__redis_conn.type(key)
        if res == 'none':
            raise Exception(f'键 {key} 不存在')
        return res

    # ============================================================
    def string_set_s(self, time: int = None, **key_value) -> bool:
        for key, value in key_value.items():
            self.__redis_conn.set(key, value, ex=time)
        return True

    def string_set_ms(self, time: int = None, **key_value) -> bool:
        for key, value in key_value.items():
            self.__redis_conn.set(key, value, px=time)
        return True

    def string_append(self, key: str, value: str) -> bool:
        return bool(self.__redis_conn.append(key, value))

    def string_getset(self, key: str, value: str) -> str:
        return self.__redis_conn.getset(key, value)

    def string_get(self, key: str) -> str:
        return self.__redis_conn.get(key)

    def string_mget(self, *keys) -> str:
        return self.__redis_conn.mget(keys)

    def string_len(self, key) -> int:
        return self.__redis_conn.strlen(key)

    # ============================================================
    def hash_set(self, key, **k_v) -> str:
        return self.hash_append(key, **k_v)

    # 追加字段和值, 如果字段名相同后面的会直接舍弃, 不会覆盖
    def hash_append(self, key_name, **k_v) -> str:
        for field, value in k_v.items():
            self.__redis_conn.hsetnx(key_name, field, value)
        return self.__redis_conn.hgetall(key_name)

    def hash_delete_fields(self, key_name, *k) -> bool:
        return bool(self.__redis_conn.hdel(key_name, k))

    def hash_get(self, key_name, k):
        return self.__redis_conn.hget(key_name, k)

    def hash_mget(self, key_name, *k):
        return self.__redis_conn.hmget(key_name, k)

    def hash_get_items(self, key_name) -> dict:
        return self.__redis_conn.hgetall(key_name)

    def hash_get_fields(self, key_name):
        return self.__redis_conn.hkeys(key_name)

    def hash_get_values(self, key_name):
        return self.__redis_conn.hvals(key_name)

    def hash_exists_field(self, key_name, k):
        return self.__redis_conn.hexists(key_name, k)

    def hash_fields_len(self, key_name):
        return len(self.hash_get_fields(key_name))

    def hash_match_field(self, key_name, field_reg):
        return self.__redis_conn.hscan(key_name, cursor=0, match=field_reg)

    # ============================================================
    def list_lpush(self, key, *values):
        values = list(values)
        values.reverse()
        return self.__redis_conn.lpush(key, *values)

    def list_rpush(self, key, *values):
        return self.__redis_conn.rpush(key, *values)

    def list_linsert(self, key, pos_value, value, before: bool = True):
        where = 'before' if before is True else 'after'
        return self.__redis_conn.linsert(key, where=where, refvalue=pos_value, value=value)

    def list_lset(self, key, index, value):
        return self.__redis_conn.lset(key, index, value)

    def list_lpop(self, key):
        return self.__redis_conn.lpop(key)

    def list_lpop_wait_s(self, *keys, time=1):
        return self.__redis_conn.blpop(keys, time)

    def list_rpop(self, key):
        return self.__redis_conn.rpop(key)

    def list_rpop_wait_s(self, *keys, time=1):
        return self.__redis_conn.brpop(keys, time)

    def list_remove_value(self, key, value, num=0, from_left=True):
        if from_left is True:
            num = abs(num)
            return self.__redis_conn.lrem(key, num, value)
        else:
            num = -abs(num)
            return self.__redis_conn.lrem(key, num, value)

    def list_trim_slice(self, key, start_index, end_index):
        return self.__redis_conn.ltrim(key, start_index, end_index)

    def list_slice(self, key, start_index, end_index):
        return self.__redis_conn.lrange(key, start_index, end_index)

    def list_index_value(self, key, index):
        return self.__redis_conn.lindex(key, index)

    # ============================================================
    def set_add(self, key, *values):
        return self.__redis_conn.sadd(key, *values)

    def set_move_value(self, from_key, to_key, value):
        return self.__redis_conn.smove(from_key, to_key, value)

    def set_random_pop(self, key):
        return self.__redis_conn.spop(key, count=1)

    def set_remove(self, key, *values):
        return self.__redis_conn.srem(key, *values)

    def set_len(self, key):
        return self.__redis_conn.scard(key)

    def set_logic_sub(self, key, *other_keys):
        self.__redis_conn.sdiff(key, *other_keys)

    def set_logic_sub_tokey(self, tokey, key, *other_keys):
        return self.__redis_conn.sdiffstore(tokey, key, *other_keys)

    def set_logic_and(self, key, *other_keys):
        return self.__redis_conn.sinter(key, *other_keys)

    def set_logic_and_tokey(self, tokey, key, *other_keys):
        return self.__redis_conn.sinterstore(tokey, key, *other_keys)

    def set_logic_or(self, key, *other_keys):
        return self.__redis_conn.sunion(key, other_keys)

    def set_logic_or_tokey(self, tokey, key, *other_keys):
        return self.__redis_conn.sunionstore(tokey, key, other_keys)

    def set_value_exists(self, key, value):
        return self.__redis_conn.sismember(key, value)

    def set_get(self, key):
        return self.__redis_conn.smembers(key)

    def set_random_get(self, key, num=1):
        return self.__redis_conn.srandmember(key, num)
    # ============================================================
    def zset_add(self, key, **s_v):
        return self.__redis_conn.zadd(key, s_v)

    def zset_value_increment(self, key, value, add_num):
        return self.__redis_conn.zincrby(key, value, add_num)

    def zset_remove(self, key, *values):
        return self.__redis_conn.zrem(key, *values)

    def zset_remove_score_range(self, key, min_score, max_score):
        return self.__redis_conn.zrangebyscore(key, min_score, max_score)

    def zset_slice(self, key, start_index, end_index, withscore=False):
        return self.__redis_conn.zrange(key, start_index, end_index, withscores=withscore)

    def zset_slice_score(self, key, min_score=None, max_score=None, start_score_no=None, end_score_no=None,
                         limit_offset=None, limit_count=None):
        return self.__redis_conn.zrangebyscore(key, min_score, max_score, limit_offset, limit_count)

    def zset_get_score_by_value(self, key, value):
        return self.__redis_conn.zscore(key, value)

    def zset_len(self, key):
        return self.__redis_conn.zcard(key)

    def zset_slice_score_count(self, key, min_score, max_score):
        return self.__redis_conn.zcount(key, min_score, max_score)

    def zset_slice_count(self, key, min_value, max_value):
        return self.__redis_conn.zlexcount(key, min_value, max_value)

    def zset_value_by_score_rank(self, key, value, reverse=False):
        if reverse is False:
            return self.__redis_conn.zrank(key, value)
        else:
            return self.__redis_conn.zrevrank(key, value)

# lz = LzRedisImp()
# lz.redis_conn.set('k1', 'v1')
# lz.redis_conn.set('k2', 'v2')
# lz.redis_conn.set('k3', 'v3')
# # print(lz.redis_conn.set('num1', 1))
#
# # print(lz.key_reset_expire_time_s('k1', 5))
# # print(lz.key_rename('k1', 'k2'))
#
# # print(lz.redis_conn.expireat('k2', datetime.datetime(2022, 12, 4, 19,52)))
#
# # print(lz.redis_conn.append('k1', 'vv'))
#
# pool = redis.ConnectionPool(host='127.0.0.1', port=6379,
#                             password=None, db=0, decode_responses=True, max_connections=10)
# conn = redis.Redis(connection_pool=pool, decode_responses=True)
#
# # conn.delete('hkey1')
# # conn.delete('hash2')
# # conn.hset('hkey1', 'f1', 'v1')
# # conn.hset(name="hash2", key='f1', value='v1', mapping={"k2": "v2", "k3": "v3"})
#
#
# # conn.execute_command('HMSET', 'hash2', **{"k2": "v2", "k3": "v3"})
#
# # lz.hash_append('hash2', field1='vv', field2='v2')
# #
# # print(conn.hgetall('hash2'))
# #
# # print(lz.hash_exists_field('hash2', 'field1'))
#
# # print(lz.list_lpush('lis1', 'v1', 'v2', 'v3'))
#
# print(lz.list_linsert('lis1', 'v1', 'vv', before=False))
#
# print(lz.list_slice('lis1', 0, -1))
