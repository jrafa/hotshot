# -*- coding: utf-8 -*-

import re
import redis
import urllib2
from bs4 import BeautifulSoup
from datetime import datetime


url = 'http://www.x-kom.pl'

FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S.%f'

redis_server = redis.Redis(host='localhost', port=6379)


def get_number(number):
	number = re.sub(r'\s+', '', number, flags=re.UNICODE)
	return float(number.replace(',', '.')[:-2])


def get_element(soup, tag, class_name):
	return soup.find(tag, {'class': class_name}).get_text()


def get_data(url):
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')

	title = get_element(soup, 'p', 'product-name')
	price = get_element(soup, 'div', 'new-price')
	price_first = get_element(soup, 'div', 'old-price')

	return { 'title': title.encode('utf-8'), 'price': get_number(price), 'price_first': get_number(price_first), 'date': datetime.now()}


def save_to_db():
	item = get_data(url)
	date = item['date'].strftime(FORMAT_DATETIME)
	redis_server.hmset(date, item)


def show_all():
	keys = redis_server.keys()

	for i, key in enumerate(keys):
		print '{}: {}'.format(i, redis_server.hgetall(key))


if __name__ == '__main__':
	save_to_db()
	# show_all()
