import json
from oxr import OXR
from datetime import datetime
from constants import DATE_FORMAT, DATE_HEADER_KEY, DATE_KEY, ETAG_KEY, TIMESTAMP_KEY, VALUE_KEY


class MockOXR(OXR):

    def __init__(self) -> None:
        super().__init__(app_id='')

    def get_latest_data(self, existing_etag=None, existing_date_header=None):
        res = json.loads(
            '{"disclaimer":"Usage subject to terms: https://openexchangerates.org/terms","license":"https://openexchangerates.org/license","timestamp":1659977997,"base":"USD","rates":{"BRL":4.9416}}'
        )
        return {
            TIMESTAMP_KEY: res["timestamp"],
            VALUE_KEY: res['rates']['BRL'],
            DATE_HEADER_KEY: 'Tue, 18 Apr 2023 13:15:43 GMT',
            ETAG_KEY: '123456789'
        }

    def get_historical_data(self, date):
        res = json.loads(
            '{"disclaimer":"Usage subject to terms: https://openexchangerates.org/terms","license":"https://openexchangerates.org/license","timestamp":1659977997,"base":"USD","rates":{"BRL":4.1016}}'
        )
        return {DATE_KEY: date, VALUE_KEY: res['rates']['BRL']}
