import json
from datetime import datetime
# import requests

DATE_FORMAT = "%Y-%m-%d"

class OXR:
    def __init__(self, app_id) -> None:
        self.app_id = app_id
    
    def get_latest_data(self):
        # url = 'https://openexchangerates.org/api/latest.json?app_id={app_id}&symbols={symbols}'
        # response = requests.get(url.format(app_id=app_id, symbols='BRL'))
        # data = response.json()
        res = json.loads('{"disclaimer":"Usage subject to terms: https://openexchangerates.org/terms","license":"https://openexchangerates.org/license","timestamp":1659977997,"base":"USD","rates":{"BRL":5.5516}}')
        date = datetime.utcfromtimestamp(res["timestamp"]).strftime(DATE_FORMAT)
        return {'date': date, 'value': res['rates']['BRL'] }

    # https://openexchangerates.org/api/historical/:date.json?app_id={app_id}&symbols={symbols}
    # YYYY-MM-DD
    def get_historical_data(self, date):
        res = json.loads('{"disclaimer":"Usage subject to terms: https://openexchangerates.org/terms","license":"https://openexchangerates.org/license","timestamp":1659977997,"base":"USD","rates":{"BRL":5.1016}}')
        if not res:
            raise "Error"
        return {'date': date, 'value': res['rates']['BRL'] }
