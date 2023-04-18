from tinydb import TinyDB, Query
from constants import DATE_HEADER_KEY, ETAG_KEY, TIMESTAMP_KEY, VALUE_KEY, DATE_KEY


class DB:

    def __init__(self, file_name: str) -> None:
        self.__db = TinyDB(file_name)
        self.__cotacoes = self.__db.table('cotacoes')
        self.__historico = self.__db.table('historico')

    def save_historical_data(self, date, value) -> None:
        Record = Query()
        self.__historico.upsert({
            DATE_KEY: date,
            VALUE_KEY: value
        }, Record.date == date)

    def get_historical_data(self, date) -> float | None:
        Record = Query()
        record = self.__historico.get(Record.date == date)
        if record is None:
            return

        return record[VALUE_KEY]

    def save_current_value(self, etag, date_header, timestamp, value) -> None:
        self.__cotacoes.insert({
            ETAG_KEY: etag,
            DATE_HEADER_KEY: date_header,
            TIMESTAMP_KEY: timestamp,
            VALUE_KEY: value
        })

    def get_last_stored_value(self):
        all_records = self.__cotacoes.all()
        if len(all_records) == 0:
            return

        return all_records[-1]
