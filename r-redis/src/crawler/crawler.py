from time import sleep

import requests
from bs4 import BeautifulSoup

from redis_connection import RedisDatabase

redis = RedisDatabase()


def push_links(url='https://www.varzesh3.com'):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            sleep(2)
            redis.client.rpush('links', href)


if __name__ == '__main__':
    push_links()
