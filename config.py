import os

ENVIRONMENT = "dev"
DEBUG = True

HOST = "127.0.0.1"
PORT = 5000

USE_STALE_OK = True
COUCHDB_SERVER = "localhost:8080"

COUCHDB_USER_DB = "test-users"
COUCHDB_MUSIC_DB = "test-music"
COUCHDB_EVENTS_DB = "test-events"
COUCHDB_CHAINED_EVENTS_DB = "test-chained-events"

SECRET_KEY = "this_secret_key"

# let custom config override defaults
if os.environ.get('FOOD_TRUCK_CONFIG', False):
    import imp
    imp.load_source('app.customconfig',
        os.environ['FOOD_TRUCK_CONFIG'])
    from app.customconfig import *