import requests
from datetime import datetime
from constants import DATE_FORMAT


class OXR:
    def __init__(self, app_id) -> None:
        self.__app_id = app_id

    def get_latest_data(self):
        url = 'https://openexchangerates.org/api/latest.json?app_id={app_id}&symbols={symbols}'
        response = requests.get(url.format(
            app_id=self.__app_id, symbols='BRL'))
        res = response.json()
        date = datetime.utcfromtimestamp(
            res["timestamp"]).strftime(DATE_FORMAT)
        return {'date': date, 'value': res['rates']['BRL']}

    def get_historical_data(self, date):
        url = 'https://openexchangerates.org/api/historical/{date}.json?app_id={app_id}&symbols={symbols}'
        response = requests.get(url.format(
            app_id=self.__app_id, date=date, symbols='BRL'))
        res = response.json()
        return {'date': date, 'value': res['rates']['BRL']}
