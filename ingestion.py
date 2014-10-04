import csv
import logging
import urllib2

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_hours(schedule_key, schedule_value):
    if schedule_key == "Hours":
        print schedule_value
        return schedule_key, schedule_value
    return schedule_key, schedule_value

# Parse the response
def get_schedule(permit_number, location_id):
    '''
    Convert the extracted information into proper time stamps
    Military Time is going to be used.
    The times are going to changed to the following,
    morning = 6am - 10am
    Lunch = 10am -
    '''
    json_url = "http://bsmnt.sfdpw.org/ArcGIS/rest/services/MobileFoodPermits/MapServer/0/query?f=json&where=DataField%20%3D%20%27{}%27&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=DataField%2CLocationID%2CInfoField".format(permit_number)
    r = requests.get(json_url)
    locations = r.json()

    for item in locations['features']:
        if item['attributes']['LocationID'] == location_id:
            schedule_dict = {}
            for key_value in item['attributes']['InfoField'].split(","):
                if "FoodItems" not in key_value:
                    try:
                        temp_key, temp_value = key_value.split(": ")
                        temp_key, temp_value = convert_hours(temp_key, temp_value)
                        schedule_dict[temp_key] = temp_value
                    except ValueError:
                        logger.warning("Value doesn't contain a semicolon")

                else:
                    schedule_dict["FoodItems"] = key_value.replace("FoodItems: ", "")
            return schedule_dict

def ingest_csv_file():
    '''
    Each line links to a PDF with a specific schedule on the food truck.
    It appears that the location modifies according to the date.
    '''
    csv_url = "https://data.sfgov.org/api/views/px6q-wjh5/rows.csv?accessType=DOWNLOAD"
    response = urllib2.urlopen(csv_url)
    master_doc = csv.DictReader(response)
    for row in master_doc:
        schedule = get_schedule(row['permit'], int(row['locationid']))

logging.info("Creating local database")
ingest_csv_file()