import json
import os
from time import sleep
from database import DB
from datetime import datetime, date, timedelta
from dotenv import load_dotenv

from oxr import OXR

load_dotenv()

DATE_FORMAT = "%Y-%m-%d"

def get_last_day():
    weekend_threshold = get_weekend_threshold()
    last_day = (date.today() - timedelta(days=weekend_threshold)).strftime(DATE_FORMAT)
    return last_day

def get_weekend_threshold():
    today = date.today().weekday()
    if today == 6: # Sunday
        return 2
    elif today == 5: # Saturday
        return 1
    else:
        return 0

def percentage_diff(previous, current):
    try:
        percentage = (abs(previous - current)/previous) * 100
    except ZeroDivisionError:
        percentage = float('inf')
    return percentage

def is_greater_than(threshold, a, b):
    return percentage_diff(a, b) > threshold

# get value from last day (database, or call api if not found)
# get value from today (api, store in database
# compare last day value with today
# if diff > 5% open up web browser
app_id = os.getenv('APP_ID')
api = OXR(app_id)
db = DB("historical_data.json", api)
last_day = get_last_day()
last_day_value = db.get_historical_value(last_day)

while True:
    response = api.get_latest_data()
    latest_date = response['date']
    latest_value = response['value']
    db.store_historical_data(latest_date, latest_value)

    diff = percentage_diff(last_day_value, latest_value)
    if diff > 5:
        print("Diff maior que 5%: Valor Atual = " + str(latest_value) + " Diff: " + str(diff))
    else:
        print("Não foi dessa vez - Diff: ", diff)
    
    sleep(15 * 60) # 15 minutos
