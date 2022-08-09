from tinydb import TinyDB, Query
from constants import VALUE_KEY, DATE_KEY


class DB:
    def __init__(self, file_name: str) -> None:
        self.__db = TinyDB(file_name)

    def store_historical_data(self, date: str, value) -> None:
        Record = Query()
        self.__db.upsert({DATE_KEY: date, VALUE_KEY: value},
                         Record.date == date)

    def get_historical_value(self, date: str):
        Record = Query()
        # Returns first occurence only
        res = self.__db.get(Record.date == date)
        if res:
            return res[DATE_KEY]
        else:
            return None
