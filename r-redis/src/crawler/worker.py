import sys

from redis_connection import RedisDatabase

redis = RedisDatabase()


def watch_links_data(worker_name):
    print(f'Worker {worker_name} Stared')
    while True:
        link = redis.client.blpop(keys='links')  # Block and Left Pop
        print(f'Link: {link}')
    # print(f'Worker {worker_name} Ended')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise KeyError('Worker name is required')
    watch_links_data(worker_name=sys.argv[1])
