import couchdb

from app import app


def gmaps_api():
    return app.config['GOOGLE_API_KEY']

def server_connection():
    couch = couchdb.Server(app.config['COUCHDB_SERVER'])
    return couch