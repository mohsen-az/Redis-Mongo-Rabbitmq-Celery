import random

from redis_connection import RedisDatabase

redis = RedisDatabase()


def import_users_data(count=100000):
    """
    Write speed for 100000 data: 5.079s
    :param count:
    :return:
    """
    for index in range(count):
        redis.client.set(
            name=f'user:score:{index}',
            value=random.randint(1, 10)
        )
    print(f'{count} users recorded imported successfully.')


if __name__ == '__main__':
    import_users_data()
