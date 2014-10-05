import couchdb

from app import app


def gmaps_api():
    return app.config['GOOGLE_API_KEY']

def server_connection():
    '''
    Not including server location since, this is deployed to localhost for now
    '''
    couch = couchdb.Server()
    return couch

def get_truck_db():
    '''
    The Try Except isn't necessary, but since I'm not developing the dev-ops portion of it
    Making sure the Database is actually there before connecting to it.
    '''
    couch = server_connection()
    try:
        db = couch[app.config['TRUCK_DB']]
    except:
        db = couch.create(app.config['TRUCK_DB'])

    return db