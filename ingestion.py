import csv
import logging
import urllib2

from dateutil import parser, relativedelta
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def time_in_sequence(start_time, end_time):
    '''
    function takes a range of time and emits every hour in them
    Breakfast = 6am - 11am
    Lunch = 11am - 4pm
    Dinner = 4pm - Onwards
    '''
    start_time = parser.parse(start_time)
    end_time = parser.parse(end_time)
    start_morning = parser.parse("6AM")
    end_morning = parser.parse("11AM")
    start_afternoon = parser.parse("11AM")
    end_afternoon = parser.parse("4PM")
    start_evening = parser.parse("4PM")
    end_evening = parser.parse("11PM")
    allowed_morning = False
    allowed_afternoon = False
    allowed_evening = False
    allowed_late = False
    if end_time < start_time:
        allowed_late = True
    while start_time <= end_time:
        if start_morning <= start_time <= end_morning:
            allowed_morning = True
        elif start_afternoon <= start_time <= end_afternoon:
            allowed_afternoon = True
        elif start_evening <= start_time < end_evening:
            allowed_evening = True
        else:
            allowed_late = True

        start_time += relativedelta.relativedelta(hours=+1)

    return {"morning": allowed_morning,
            "afternoon": allowed_afternoon,
            "evening": allowed_evening,
            "late_night": allowed_late}

def change_date(schedule_value):
    '''
    Making the parsing of the information into it's separate
    '''
    day_array = ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")
    temp_schedule = {"Mo": None,
                     "Tu": None,
                     "We": None,
                     "Th": None,
                     "Fr": None,
                     "Sa": None,
                     "Su": None}
    days, hours = schedule_value.split(":")
    if len(days) == 2 and "/" not in hours:
        start_time, end_time = hours.split("-")
        time_schedule = time_in_sequence(start_time, end_time)
        temp_schedule[days] = time_schedule
    elif "-" in days and len(days) == 5 and "/" not in hours:
        start_time, end_time = hours.split("-")
        time_schedule = time_in_sequence(start_time, end_time)
        start_day, end_day = days.split("-")
        seen_start_date = False
        for day in day_array:
            if day == start_day:
                seen_start_date = True
                temp_schedule[day] = time_schedule
            elif seen_start_date and end_day != day:
                temp_schedule[day] = time_schedule
            elif seen_start_date and end_day == day:
                temp_schedule[day] = time_schedule
                break
    elif "-" in days and len(days) == 5 and "/" in hours and "-" in hours:
        batches_of_times = hours.split("/")
        master_time_schedule = {"morning": False,
                                "afternoon": False,
                                "evening": False}
        for batch in batches_of_times:
            start_time, end_time = batch.split("-")
            time_schedule = time_in_sequence(start_time, end_time)
            for key in master_time_schedule:
                if time_schedule[key] > master_time_schedule[key]:
                    master_time_schedule[key] = time_schedule[key]
                else:
                    continue

        start_day, end_day = days.split("-")
        seen_start_date = False
        for day in day_array:
            if day == start_day:
                seen_start_date = True
                temp_schedule[day] = master_time_schedule
            elif seen_start_date and end_day != day:
                temp_schedule[day] = master_time_schedule
            elif seen_start_date and end_day == day:
                temp_schedule[day] = master_time_schedule
                break

    elif "/" in days and "-" not in days and "-" in hours and "/" not in hours:
        start_time, end_time = hours.split("-")
        time_schedule = time_in_sequence(start_time, end_time)
        for day in days.split("/"):
            temp_schedule[day] = time_schedule

    elif "/" in days and "-" not in days and "-" in hours and "/" in hours:
        batches_of_times = hours.split("/")
        master_time_schedule = {"morning": False,
                                "afternoon": False,
                                "evening": False}
        for batch in batches_of_times:
            start_time, end_time = batch.split("-")
            time_schedule = time_in_sequence(start_time, end_time)
            for key in master_time_schedule:
                if time_schedule[key] > master_time_schedule[key]:
                    master_time_schedule[key] = time_schedule[key]
                else:
                    continue
        for day in days.split("/"):
            temp_schedule[day] = master_time_schedule

    else:
        logging.warning("Couldn't transform the following date {}".format(schedule_value))
    return temp_schedule

def convert_hours(schedule_key, schedule_value):
    '''
    Breakfast = 6am - 11am
    Lunch = 11am - 4pm
    Dinner = 4pm - Onwards
    The website offers a horrible way of parsing the data, which is fine;
    however, I'm building my own parser which attempts to file it in a different order.
    '''
    if schedule_key == "Hours":
        if ";" not in schedule_value:
            temp_schedule = change_date(schedule_value)
        else:
            master_temp_schedule = {"Mo": None,
                                    "Tu": None,
                                    "We": None,
                                    "Th": None,
                                    "Fr": None,
                                    "Sa": None,
                                    "Su": None}
            for dates in schedule_value.split(";"):
                new_schedule = change_date(dates)
                for key in master_temp_schedule:
                    if master_temp_schedule[key] is None:
                        master_temp_schedule[key] = new_schedule[key]
                    else:
                        m_temp = master_temp_schedule[key]
                        t_temp = new_schedule[key]
                        for inner_key in m_temp:
                            if t_temp[inner_key] > m_temp[inner_key]:
                                m_temp[inner_key] = t_temp[inner_key]
                            else:
                                continue
                        master_temp_schedule[key] = m_temp
            temp_schedule = master_temp_schedule

        return schedule_key, temp_schedule
    return schedule_key, schedule_value


def get_schedule(permit_number, location_id):
    '''
    Convert the extracted information into proper time stamps
    Military Time is going to be used.
    The times are going to changed to the following,
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
        print schedule

logging.info("Creating local database")
ingest_csv_file()

