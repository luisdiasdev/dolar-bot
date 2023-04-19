import requests
from constants import DATE_FORMAT, DATE_HEADER_KEY, DATE_KEY, ETAG_KEY, TIMESTAMP_KEY, VALUE_KEY
from logging import getLogger

logger = getLogger(__name__)


class OXR:

    def __init__(self, app_id) -> None:
        self.__app_id = app_id

    def get_latest_data(self, existing_etag=None, existing_date_header=None):
        logger.debug('fetching latest data from oxr. etag:%s - date:%s',
                     existing_etag, existing_date_header)
        headers = {}
        if existing_etag is not None and existing_date_header is not None:
            headers = {
                "If-None-Match": existing_etag,
                "If-Modified-Since": existing_date_header
            }

        url = 'https://openexchangerates.org/api/latest.json?app_id={app_id}&symbols={symbols}'
        response = requests.get(url.format(app_id=self.__app_id,
                                           symbols='BRL'),
                                headers=headers)
        logger.debug('latest data from oxr received.')
        res = response.json()
        etag = response.headers.get('Etag')
        date_header = response.headers.get('Date')

        return {
            ETAG_KEY: etag,
            DATE_HEADER_KEY: date_header,
            TIMESTAMP_KEY: res["timestamp"],
            VALUE_KEY: res['rates']['BRL']
        }

    def get_historical_data(self, date):
        logger.debug('fetching historical data from oxr. date:%s', date)
        url = 'https://openexchangerates.org/api/historical/{date}.json?app_id={app_id}&symbols={symbols}'
        response = requests.get(
            url.format(app_id=self.__app_id, date=date, symbols='BRL'))
        res = response.json()
        value = res['rates']['BRL']
        logger.debug('historical data received from oxr. date:%s value:%f',
                     date, value)
        return {DATE_KEY: date, VALUE_KEY: value}
