"""
    Redis封装工具类
   @author TinaRoot
   @since 2022/3/4 下午3:22
"""

from aiapp import setting
import redis

logger = setting.LogConfig.logger

# Redis链接地址
HOST = "10.0.20.7"
# HOST = "127.0.0.1"
PORT = "19763"
PASSWORD = "Redis@1003"


class redisClient:
    """
    py2.7, py3.4
    """

    # mutex = threading.Lock()  # gevent 里使用线程锁可能有问题
    connection_pool = None
    connection_client = None

    def __init__(self):
        """
        :param config: {"host":"",
                        "port": 0,
                        "index": 0,
                        "auth": "",
                        "encoding": "",
                        "decode_responses": False,
                        "max_connections": 1,
                        "target_max_memory": 1024
                        }
        """
        config = {
            "host": HOST,
            "port": PORT,
            "auth": PASSWORD,
            "index": 0,
            "encoding": "utf-8",
            "decode_responses": True,
            "target_max_memory": 3896,
            "max_connections": 1
        }
        self.config = config
        max_conn = 1
        if "max_connections" in self.config:
            max_conn = self.config["max_connections"]
            if max_conn <= 0:
                max_conn = 1
        decode_responses = False
        if "decode_responses" in config:
            decode_responses = config["decode_responses"]
        temp_pool = redis.ConnectionPool(host=self.config['host'], port=self.config['port'], db=self.config['index'],
                                         password=self.config['auth'],
                                         encoding=self.config['encoding'], max_connections=max_conn,
                                         decode_responses=decode_responses)
        self.connection_pool = temp_pool
        temp_client = redis.Redis(connection_pool=self.connection_pool)
        self.connection_client = temp_client

    def rpush(self, key, json_text, expired_in_seconds=0):
        """
        在列表中添加一个或多个值
        :param key:
        :param json_text:
        :param expired_in_seconds:
        :return:
        """
        r = self.connection_client
        # self.mutex.acquire()
        pipe = r.pipeline()
        pipe.rpush(key, json_text)
        if expired_in_seconds > 0:
            pipe.expire(key, expired_in_seconds)
        pipe.execute()
        # self.mutex.release()

    def lrange(self, key):
        """
        获取列表中所有的值
        :param key:
        """
        r = self.connection_client
        return r.lrange(key, 0, -1)

    def lpush(self, key, json_text, expired_in_seconds=0):
        """
        将一个或多个值插入到列表头部
        :param key:
        :param json_text:
        :param expired_in_seconds:
        :return:
        """
        r = self.connection_client
        # self.mutex.acquire()
        pipe = r.pipeline()
        pipe.lpush(key, json_text)
        if expired_in_seconds > 0:
            pipe.expire(key, expired_in_seconds)
        pipe.execute()
        # self.mutex.release()

    def lpop_pipline(self, key, length):
        i = 0
        poped_items = []
        r = self.connection_client
        # self.mutex.acquire()
        curent_len = r.llen(key)
        if curent_len > 0:
            target_len = 0
            if curent_len > length:
                target_len = length
            else:
                target_len = curent_len
            pipe = r.pipeline()
            while i < target_len:
                pipe.lpop(key)
                i += 1
            temp_poped_items = pipe.execute()
            poped_items = temp_poped_items
        # self.mutex.release()
        return poped_items

    def lpop(self, key):
        """
        移出并获取列表的第一个元素
        :param key:
        :return:
        """
        poped_items = []
        r = self.connection_client
        # self.mutex.acquire()
        data = r.lpop(key)
        if data:
            poped_items.append(data)
        # self.mutex.release()
        return poped_items

    def rpop_pipline(self, key, length):
        i = 0
        poped_items = []
        r = self.connection_client
        # self.mutex.acquire()
        curent_len = r.llen(key)
        if curent_len > 0:
            target_len = 0
            if curent_len > length:
                target_len = length
            else:
                target_len = curent_len
            pipe = r.pipeline()
            while i < target_len:
                pipe.rpop(key)
                i += 1
            temp_poped_items = pipe.execute()
            poped_items = temp_poped_items
        # self.mutex.release()
        return poped_items

    def rpop(self, key):
        """
        移除并获取列表最后一个元素
        :param key:
        :return:
        """
        poped_items = []
        r = self.connection_client
        # self.mutex.acquire()
        data = r.rpop(key)
        if data:
            poped_items.append(data)
        # self.mutex.release()
        return poped_items

    def hincrby(self, hash_key, field, amount=1):
        r = self.connection_client
        # self.mutex.acquire()
        result = r.hincrby(hash_key, field, amount)
        # self.mutex.release()
        return result

    def llen(self, key):
        """
        该键包含多少个元素
        :param key:
        :return:
        """
        r = self.connection_client
        # self.mutex.acquire()
        result = r.llen(key)
        # self.mutex.release()
        return result

    def hdel(self, key, field):
        """
        删除哈希值
        :param key:
        :param field:
        :return:
        """
        r = self.connection_client
        # self.mutex.acquire()
        result = r.hdel(key, field)
        # self.mutex.release()
        return result

    def hset(self, key, field, value, expired_in_seconds=0):
        """

        :param key:
        :param field:
        :param value:
        :param expired_in_seconds:
        :return:
        """
        r = self.connection_client
        # self.mutex.acquire()
        pipline = r.pipeline()
        pipline.hset(key, field, value)
        if expired_in_seconds > 0:
            pipline.expire(key, expired_in_seconds)
        pipline.execute()
        # self.mutex.release()

    def info(self, section=None):
        r = self.connection_client
        # self.mutex.acquire()
        result = r.info(section)
        # self.mutex.release()
        return result

    def exceed_memory_limits(self):
        result = False
        if "target_max_memory" in self.config.keys():
            target_max_memory = self.config["target_max_memory"]
            redis_info = self.info("memory")
            distance = self.__max_memory_distance(redis_info, target_max_memory)
            if distance and distance <= 0:
                result = True
        return result

    def __max_memory_distance(self, redis_info_dict, target_max):
        # # Memory
        # used_memory:472978192
        # used_memory_human:451.07M
        # used_memory_rss:510640128
        # used_memory_peak:493548568
        # used_memory_peak_human:470.68M
        # used_memory_lua:35840
        # mem_fragmentation_ratio:1.08
        # mem_allocator:jemalloc - 3.6.0
        result = None
        if "used_memory" in redis_info_dict.keys():
            temp_used = int(redis_info_dict["used_memory"])
            temp_used = temp_used / (1024 * 1024)
            result = target_max - temp_used
        else:
            logger.warning(u"未找到已用内存！")
        return result

    def sadd(self, key, value):
        """
        向集合中添加单个或多个元素
        :param key:
        :param value:
        :return:
        """
        r = self.connection_client
        # self.mutex.acquire()
        result = r.sadd(key, value)
        # self.mutex.release()
        return result

    def sismember(self, key, value):
        """
        该函数得到集合内所有的元素，返回一个普通的集合
        :param key:
        :param value:
        :return:
        """
        r = self.connection_client
        # self.mutex.acquire()
        result = r.sismember(key, value)
        # self.mutex.release()
        return result

    def exists(self, key):
        """
        判断key是否存在
        :param key:
        :return:
        """
        r = self.connection_client
        # self.mutex.acquire()
        result = r.exists(key)
        # self.mutex.release()
        return result

    def keys(self, pattern):
        r = self.connection_client
        # self.mutex.acquire()
        result = r.keys(pattern=pattern)
        # self.mutex.release()
        return result

    def delele(self, key):
        """
        删除key
        :param key:
        :return:
        """
        r = self.connection_client
        # self.mutex.acquire()
        r.delete(key)
        # self.mutex.release()

    def scan(self, cursor, match=None, count=50):
        """
        :param cursor:
        :param match:
        :param count:
        :return:
         (new_cursor,
            [key1, key2, key3 ...])
        """
        r = self.connection_client
        # self.mutex.acquire()
        result = r.scan(cursor=cursor, match=match, count=count)
        # self.mutex.release()
        return result

    def hmget(self, hash_key, fields_list):
        r = self.connection_client
        # self.mutex.acquire()
        result = r.hmget(hash_key, fields_list)
        # self.mutex.release()
        return result

    def set(self, key, value, ex=None):
        """
        设置值
        :param key: 键
        :param value:  值
        :param ex: 过期时间 秒
        :return:
        """
        r = self.connection_client
        # self.mutex.acquire()
        result = r.set(key, value, ex)
        # self.mutex.release()
        return result

    def get(self, key):
        """
        获取值
        :param key: 键
        :return:
        """
        r = self.connection_client
        # self.mutex.acquire()
        result = r.get(key)
        # self.mutex.release()
        return result

    def incr(self, key):
        """
        自增ID
        :param key: 主键
        :return:  自增值 阿拉伯数字
        """
        r = self.connection_client
        result = r.incr(key, amount=1)
        return result

    def expireTime(self, key, ex):
        """
        设置过期时间
        :param key: 主键
        :param ex: 过期时间【秒】
        """
        r = self.connection_client
        result = r.expire(key, ex)
        return result

    #     关闭连接
    def close(self):
        if self.connection_pool:
            self.connection_pool.disconnect()


redis_client = redisClient()

if __name__ == "__main__":
    redis_client.set('name', 'tinaroot')
    # print(redis_client.expireTime("tina",10))
    print(redis_client.exists('name'))
    # redis_client.delele("tina")
    # print(redis_client.incr("tina"))
