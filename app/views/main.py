import connections

from flask import render_template


def google_maps():
    API_KEY = connections.gmaps_api()
    return render_template('index.html',
                           API_KEY=API_KEY)