from datetime import datetime

from flask import request, jsonify
from pytz import timezone

from connections import get_truck_db

def open():
    day_array = ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")
    time = request.args.get('time')
    day = day_array[datetime.now(tz=timezone('US/Pacific')).weekday()]
    db = get_truck_db()
    trucks = db.view('distance/approved', startkey=[day, time], endkey=[day, time, {}])
    results = []
    for truck in trucks:
        results.append(tuple(truck.value))
    return jsonify({"results": results})