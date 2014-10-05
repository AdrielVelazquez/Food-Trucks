import os

ENVIRONMENT = "dev"
DEBUG = True

HOST = "127.0.0.1"
PORT = 5000
GOOGLE_API_KEY = "AIzaSyCXO_PlJBhg5i46aIJ3opoIINOoBPa67v4"
COUCHDB_SERVER = "https://adriel.cloudant.com/"
COUCHDB_SERVER_USERNAME = "adriel"
COUCHDB_SERVER_PASSWORD = "Demons88"
TRUCK_DB = "truck-db"

# let custom config override defaults
if os.environ.get('FOOD_TRUCK_CONFIG', False):
    import imp
    imp.load_source('app.customconfig',
        os.environ['FOOD_TRUCK_CONFIG'])
    from app.customconfig import *