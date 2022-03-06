from time import sleep

import requests as requests
from bs4 import BeautifulSoup


def crawl_links(url="https://www.varzesh3.com"):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            sleep(2)
            yield href
