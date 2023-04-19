from tinydb import TinyDB, Query
from constants import DATE_HEADER_KEY, ETAG_KEY, TIMESTAMP_KEY, VALUE_KEY, DATE_KEY
from logging import getLogger

logger = getLogger(__name__)


class DB:

    def __init__(self, file_name: str) -> None:
        self.__db = TinyDB(file_name)
        self.__cotacoes = self.__db.table('cotacoes')
        self.__historico = self.__db.table('historico')

    def save_historical_data(self, date, value) -> None:
        Record = Query()
        logger.debug('saving historical data [%s] -> %f', date, value)
        self.__historico.upsert({
            DATE_KEY: date,
            VALUE_KEY: value
        }, Record.date == date)
        logger.debug('historical data saved.')

    def get_historical_data(self, date) -> float | None:
        Record = Query()
        logger.debug('getting historical data for date: [%s]', date)
        record = self.__historico.get(Record.date == date)
        if record is None:
            logger.debug('no historical date found for date: [%s]', date)
            return

        value = record[VALUE_KEY]
        logger.debug('found historical date: [%s] -> %f', date, value)
        return value

    def save_current_value(self, etag, date_header, timestamp, value) -> None:
        logger.debug('saving real time value. %s - %f - %s - %s', timestamp,
                     value, etag, date_header)
        self.__cotacoes.insert({
            ETAG_KEY: etag,
            DATE_HEADER_KEY: date_header,
            TIMESTAMP_KEY: timestamp,
            VALUE_KEY: value
        })
        logger.debug('saved real time value.')

    def get_last_stored_value(self):
        logger.debug('getting last stored value from database')
        all_records = self.__cotacoes.all()
        if len(all_records) == 0:
            logger.debug('no records found in database')
            return

        last_stored_value = all_records[-1]
        logger.debug('found records. returning last stored value. %s - %f',
                     last_stored_value[TIMESTAMP_KEY],
                     last_stored_value[VALUE_KEY])
        return last_stored_value
