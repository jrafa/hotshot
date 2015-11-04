# -*- coding: utf-8 -*-

"""
    Script is responsible for scraping data from website and save data in redis.
"""

import re
import redis
import urllib2
from bs4 import BeautifulSoup
from datetime import datetime


WEBSITE = 'http://www.x-kom.pl'

FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S.%f'

REDIS_SERVER = redis.Redis(host='localhost', port=6379)


def get_number(number):
    """
    Convert string to float and replace comma to dot.
    :param number: string
    :return: float
    """
    number = re.sub(r'\s+', '', number, flags=re.UNICODE)
    return float(number.replace(',', '.')[:-2])


def get_element(soup, tag, class_name):
    """
    Find element in website and return data. For example title, price.
    :param soup:
    :param tag:
    :param class_name:
    :return:
    """
    return soup.find(tag, {'class': class_name}).get_text()


def get_data(url):
    """
    Function open and read website. Find title and price.
    :param url: WEBSITE
    :return: dictionary with data
    """
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    title = get_element(soup, 'p', 'product-name')
    price = get_element(soup, 'div', 'new-price')
    price_first = get_element(soup, 'div', 'old-price')

    return {'title': title.encode('utf-8'), 'price': get_number(price), 'price_first': get_number(price_first), 'date': datetime.now()}


def save_to_db():
    """
    Save data to redis.
    :return:
    """
    item = get_data(WEBSITE)
    date = item['date'].strftime(FORMAT_DATETIME)
    REDIS_SERVER.hmset(date, item)


def show_all():
    """
    Display data (key, value) from redis.
    :return:
    """
    keys = REDIS_SERVER.keys()

    for i, key in enumerate(keys):
        print '{}: {}'.format(i, REDIS_SERVER.hgetall(key))


if __name__ == '__main__':
    save_to_db()
    # show_all()
