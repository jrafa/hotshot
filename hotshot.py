# -*- coding: utf-8 -*-

"""
    Simple flask application displays data from database. Module with views.
"""

from flask import Flask, render_template, request, redirect, url_for
from shot import REDIS_SERVER
from datetime import date, datetime
import time
import settings


app = Flask(__name__)
app.debug = settings.DEBUG


FORMAT_CALENDAR = '%d.%m.%Y'


FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S.%f'


FORMAT_DATETIME_FILTER = '%d-%m-%Y %H:%M'


@app.template_filter('strftime')
def filter_datetime(date):
    """
    Template tag changes format datetime.
    :param date:
    :return:
    """
    return datetime.strptime(date, FORMAT_DATETIME).strftime(FORMAT_DATETIME_FILTER)


def convert_to_date(date_to_convert, format_date):
    """
    Function convert string to date.
    :param date_to_convert: string
    :param format_date: string
    :return: date
    """
    time_to_convert = time.strptime(date_to_convert, format_date)
    return date(*time_to_convert[:3])


def check_date(date_to_check, date_from, date_to):
    """
    Check if the date is between range of dates.
    :param date_to_check: string
    :param date_from: string
    :param date_to: string
    :return: True or False
    """
    date_from = convert_to_date(date_from, FORMAT_CALENDAR)
    date_to = convert_to_date(date_to, FORMAT_CALENDAR)
    if date_from > date_to:
        return False
    return date_to >= convert_to_date(date_to_check, FORMAT_DATETIME) >= date_from


def get_hotshots(date_filter=False, date_from=None, date_to=None):
    """
    Function return sorted data from redis. Function can also return sorted data by date.
    :param date_filter: True or False (default)
    :param date_from: string
    :param date_to: string
    :return: list
    """
    keys = REDIS_SERVER.keys()

    if date_filter:
        keys = [key for key in keys if check_date(key, date_from, date_to)]

    items = []

    for key in keys:
        hotshot = REDIS_SERVER.hgetall(key)
        hotshot['title'] = unicode(hotshot.get('title'), 'utf-8')
        items.append(hotshot)

    items.sort(reverse=True)

    return items


@app.route('/', methods=['GET'])
def index():
    """
    View displays list of hotshots.
    :return:
    """
    items = get_hotshots()
    return render_template('index.html', hotshots=items)


@app.route('/hotshots', methods=['POST'])
def hotshots():
    """
    View displays results filtered by date.
    :return:
    """
    if request.method == 'POST':

        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')

        if date_from and date_to:
            items = get_hotshots(True, date_from, date_to)

            return render_template('index.html', hotshots=items)

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    """
    View which handle error 404 page not found.
    :param e:
    :return:`
    """
    return render_template('error.html', error_404=True), 404


@app.errorhandler(500)
def exception_handler(e):
    """
    View which handle error 500 internal server error.
    :param e:
    :return:
    """
    return render_template('error.html', error_500=True), 500


if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT_APP)
