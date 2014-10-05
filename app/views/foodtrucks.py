from datetime import datetime

from flask import request
from pytz import timezone

from connections import get_truck_db


def open():
    day_array = ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")
    time = request.args.get('time')
    pacific_day = datetime.now(tz=timezone('US/Pacific')).weekday()
    day = day_array[pacific_day]
    for i in range(100):
        print day, time
    db = get_truck_db()

    return True