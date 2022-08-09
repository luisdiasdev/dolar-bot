import os
from time import sleep
from constants import DATE_FORMAT, VALUE_KEY, DATE_KEY
from database import DB
from datetime import date, timedelta
from oxr import OXR
from mock_oxr import MockOXR


def get_last_day():
    weekend_threshold = get_weekend_threshold()
    last_day = (date.today() - timedelta(days=weekend_threshold)
                ).strftime(DATE_FORMAT)
    return last_day


def get_weekend_threshold():
    today = date.today().weekday()
    if today == 6:  # Sunday
        return 2
    elif today == 5:  # Saturday
        return 1
    else:
        return 0


def percentage_diff(previous, current):
    try:
        percentage = (abs(previous - current)/previous) * 100
    except ZeroDivisionError:
        percentage = float('inf')
    return percentage


class DolarBot:
    def __init__(self, threshold, mock_api) -> None:
        self.__app_id = os.getenv('APP_ID')
        self.__api = MockOXR() if mock_api else OXR(self.__app_id)
        self.__db = DB("data/historical_data.json")
        self.__threshold = threshold

    def watch(self) -> None:
        last_day = get_last_day()
        last_day_value = self.__db.get_historical_value(last_day)

        if last_day_value is None:
            api_res = self.__api.get_historical_data(last_day)
            last_day_value = api_res[VALUE_KEY]
            self.__db.store_historical_data(last_day, last_day_value)

        while True:  # Find out better way to stop this later (maybe threads?)
            response = self.__api.get_latest_data()
            latest_date = response[DATE_KEY]
            latest_value = response[VALUE_KEY]
            self.__db.store_historical_data(latest_date, latest_value)

            if self.__has_crossed_threshold(last_day_value, latest_value):
                print("Diff maior que 5%: Valor Atual = " +
                      str(latest_date) + " Diff > " + str(self.__threshold))
                # DO something fun, send email or whatever
            else:
                print("Não foi dessa vez - Diff: ")

            sleep(15 * 60)

    def __has_crossed_threshold(self, old_value, new_value):
        diff = percentage_diff(old_value, new_value)
        return diff > self.__threshold
