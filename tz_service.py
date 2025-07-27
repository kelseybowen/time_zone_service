import json
import zmq
from datetime import *
from dateutil.tz import *
from uszipcode import SearchEngine
from zoneinfo import ZoneInfo

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def get_time_zone_name(zip):
    sr = SearchEngine()
    return sr.by_zipcode(zip).timezone

def get_time_in_search_timezone(tz_name):
    tz = ZoneInfo(tz_name)
    return datetime.now(tz)

def calculate_time_difference(datetime_at_zip):
    there_hour = datetime_at_zip.time().hour
    here_hour = datetime.time(datetime.now()).hour
    return there_hour - here_hour

def create_json(dt_at_zip, tz_abbreviation, time_diff):
    current_local_time = datetime.time(datetime.now()).strftime("%H:%M")
    data = {
        'hm_format': dt_at_zip.strftime("%H:%M"),
        'tz_abbreviation': tz_abbreviation,
        'time_difference': time_diff,
        'local_time': current_local_time
    }
    return json.dumps(data)


while True:
    message = socket.recv()
    search_zip = message.decode()
    print(search_zip)
    
    timezone_name = get_time_zone_name(search_zip)
    dt_at_zip = get_time_in_search_timezone(timezone_name)

    tz_abbreviation = dt_at_zip.tzname()
    time_diff = calculate_time_difference(dt_at_zip)
    json_data = create_json(dt_at_zip, tz_abbreviation, time_diff)
    print(json_data)
    socket.send_string(json_data)

context.destroy()

