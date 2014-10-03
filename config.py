import os

ENVIRONMENT = "dev"
DEBUG = True

HOST = "127.0.0.1"
PORT = 5000

COUCHDB_SERVER = "localhost:8080"

# let custom config override defaults
if os.environ.get('FOOD_TRUCK_CONFIG', False):
    import imp
    imp.load_source('app.customconfig',
        os.environ['FOOD_TRUCK_CONFIG'])
    from app.customconfig import *