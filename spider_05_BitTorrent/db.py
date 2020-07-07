#!/user/bin/env python
# 每天都要有好心情
import redis

# redis key
REDIS_KEY = 'magnets'
# redis 地址
REDIS_HOST = 'localhost'
# redis port
REDIS_PORT = 6379
# redis_password
REDIS_PASSWORD = None
# redis 连接池最大连接数
REDIS_MAX_CONNECTION = 20


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        conn_pool = redis.ConnectionPool(
            host=host,
            port=port,
            password=password,
            max_connections=REDIS_MAX_CONNECTION,
        )
        self.redis = redis.Redis(connection_pool=conn_pool)

    def add_magent(self, magent):
        self.redis.sadd(REDIS_KEY, magent)

    def get_magnets(self, count=128):
        return self.redis.srandmember(REDIS_KEY, count)
