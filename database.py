from tinydb import TinyDB, Query
from constants import VALUE_KEY, DATE_KEY


class DB:

    def __init__(self, file_name: str) -> None:
        self.__db = TinyDB(file_name)
        self.__table = self.__db.table('cotacoes')

    def store_historical_data(self, date, value) -> None:
        Record = Query()
        self.__table.insert({DATE_KEY: date, VALUE_KEY: value})

    def get_last_stored_value(self):
        all_records = self.__table.all()
        if len(all_records) == 0:
            return None

        return all_records[-1][VALUE_KEY]
