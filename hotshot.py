# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, redirect, url_for
from shot import redis_server
from datetime import date
import time


app = Flask(__name__)
# app.debug = True


FORMAT_CALENDAR = '%d.%m.%Y'


FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S.%f'


def convert_to_date(date_to_convert, format):
    tm = time.strptime(date_to_convert, format)
    return date(*tm[:3])


def check_date(date_to_check, date_from, date_to):
    date_from = convert_to_date(date_from, FORMAT_CALENDAR)
    date_to = convert_to_date(date_to, FORMAT_CALENDAR)
    if date_from > date_to:
        return False
    return date_to >= convert_to_date(date_to_check, FORMAT_DATETIME) >= date_from


def get_hotshots(date_filter=False, date_from=None, date_to=None):
    keys = redis_server.keys()

    if date_filter:
        keys = [ key for key in keys if check_date(key, date_from, date_to) ]

    hotshots = []
    for key in keys:
        hotshots.append(redis_server.hgetall(key))
    hotshots.sort(reverse=True)

    return hotshots


@app.route('/', methods=['GET'])
def index():
    hotshots = get_hotshots()
    return render_template('index.html', hotshots=hotshots)


@app.route('/hotshots', methods=['POST'])
def hotshots():

    if request.method == 'POST':

        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')

        if date_from and date_to:
            hotshots = get_hotshots(True, date_from, date_to)

            return render_template('index.html', hotshots=hotshots)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6500)
