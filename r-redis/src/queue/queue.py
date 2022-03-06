from redis_connection import RedisDatabase

redis = RedisDatabase()


class Queue:
    _instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(*args, **kwargs)
        return cls._instance

    def __init__(self, queue_name='default'):
        self.connection = redis.client
        self.queue_name = queue_name

    # TODO-1: Create set for save all keys
    # TODO-2: Create list for each subscription to save adv_ids

    def push(self, list_name, value):
        self.connection.sadd(self.queue_name, list_name)
        self.connection.rpush(list_name, value)

    def pop(self, list_name, lifo):
        if lifo:
            return self.connection.rpop(list_name)
        return self.connection.lpop(list_name)

    def get_alerts(self):
        return self.connection.smembers(self.queue_name)

    def get_list_data(self, list_name):
        data = self.connection.lrange(list_name, 0, -1)
        self.connection.delete(list_name)
        return data

    def get_all_data(self):
        data = dict()
        for list_name in self.get_alerts():
            data.setdefault(list_name, self.get_list_data(list_name))

        return data
