from typing import Any
from tinydb import TinyDB, Query

from oxr import OXR

class DB:
    def __init__(self, file_name: str, api: OXR) -> None:
        self.db = TinyDB(file_name)
        self.api = api

    def store_historical_data(self, date: str, value) -> None:
        self.db.insert({ 'date': date, 'value': value })

    def get_historical_value(self, date: str):
        query = Query()
        res = self.db.search(query.date == date)
        if not res:
            api_res = self.api.get_historical_data(date)
            new_value = api_res['value']
            self.store_historical_data(date, new_value)
            return new_value
        else:
            return res[0]['value']