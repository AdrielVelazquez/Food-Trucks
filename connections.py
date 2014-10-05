import re

import couchdb

from app import app


def gmaps_api():
    return app.config['GOOGLE_API_KEY']

def server_connection():
    '''
    Not including server location since, this is deployed to localhost for now
    '''
    if app.config.get('COUCHDB_SERVER_USERNAME'):
        couch = couchdb.Server(app.config['COUCHDB_SERVER'])
        couch.resource.credentials = (app.config['COUCHDB_SERVER_USERNAME'], app.config['COUCHDB_SERVER_PASSWORD'])
    else:
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

RE_COUCH_URL = re.compile(r'^(https?)://(([_a-zA-Z0-9-]+):(.+)@)?(([a-zA-Z0-9\.-]+)(:([0-9]+))?)/([_a-zA-Z0-9-]+)/?$')
def parse_couchdb_url(s):
    """returns tuple (scheme, user, pass, host, port, dbname) or False

    user, pass & port may be returned as empty strings if not present

    >>> parse_couchdb_url("http://localhost:5984/db")
    ('http', '', '', 'localhost', '5984', 'db')
    >>> parse_couchdb_url("http://localhost:5984/db-name")
    ('http', '', '', 'localhost', '5984', 'db-name')
    >>> parse_couchdb_url("http://localhost:5984/db_name")
    ('http', '', '', 'localhost', '5984', 'db_name')
    >>> parse_couchdb_url("http://127.0.0.1:5984/db_name")
    ('http', '', '', '127.0.0.1', '5984', 'db_name')
    >>> parse_couchdb_url("http://127.0.0.1/db_name")
    ('http', '', '', '127.0.0.1', '', 'db_name')
    >>> parse_couchdb_url("https://127.0.0.1:5984/db_name")
    ('https', '', '', '127.0.0.1', '5984', 'db_name')
    >>> parse_couchdb_url("https://user:pass@127.0.0.1:5984/db_name")
    ('https', 'user', 'pass', '127.0.0.1', '5984', 'db_name')
    >>> parse_couchdb_url("https://us-er:pa-ss@127.0.0.1:5984/db_name")
    ('https', 'us-er', 'pa-ss', '127.0.0.1', '5984', 'db_name')
    >>> parse_couchdb_url("https://us-er:pa-ss@127.0.0.1/db_name/")
    ('https', 'us-er', 'pa-ss', '127.0.0.1', '', 'db_name')

    """


    match = RE_COUCH_URL.match(s)
    if match:
        m = match.groups()
        # ('https', 'user:pass@', 'user', 'pass', '127.0.0.1:5984',
        # '127.0.0.1', ':5984', '5984', 'db_name')
        scheme = m[0]
        usr = m[2] or ''
        pwd = m[3] or ''
        host = m[5]
        port = m[7] or ''
        dbname = m[8]
        return (scheme, usr, pwd, host, port, dbname)
    return False