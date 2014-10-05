from datetime import datetime

from flask import render_template
from pytz import timezone

import connections
from ingestion import time_in_sequence

def google_maps():
    pacific_time = datetime.now(tz=timezone('US/Pacific')).time()
    str_pacific_time = pacific_time.strftime("%H:%M:%S")
    current_time = time_in_sequence(str_pacific_time, str_pacific_time)
    API_KEY = connections.gmaps_api()
    return render_template('index.html',
                           API_KEY=API_KEY,
                           TIMING=current_time)