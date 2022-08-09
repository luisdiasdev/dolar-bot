
import json
from oxr import OXR
from datetime import datetime
from constants import DATE_FORMAT, DATE_KEY, VALUE_KEY


class MockOXR(OXR):
    def __init__(self) -> None:
        super().__init__(app_id='')

    def get_latest_data(self):
        res = json.loads(
            '{"disclaimer":"Usage subject to terms: https://openexchangerates.org/terms","license":"https://openexchangerates.org/license","timestamp":1659977997,"base":"USD","rates":{"BRL":5.5516}}')
        date = datetime.utcfromtimestamp(
            res["timestamp"]).strftime(DATE_FORMAT)
        return {DATE_KEY: date, VALUE_KEY: res['rates']['BRL']}

    def get_historical_data(self, date):
        res = json.loads(
            '{"disclaimer":"Usage subject to terms: https://openexchangerates.org/terms","license":"https://openexchangerates.org/license","timestamp":1659977997,"base":"USD","rates":{"BRL":5.1016}}')
        return {DATE_KEY: date, VALUE_KEY: res['rates']['BRL']}
