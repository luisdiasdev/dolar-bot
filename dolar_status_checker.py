from time import time

import telegram
from constants import DATE_FORMAT, DATE_HEADER_KEY, ETAG_KEY, TIMESTAMP_KEY, VALUE_KEY, DATE_KEY
from database import DB
from datetime import date, datetime, timedelta
from oxr import OXR
from mock_oxr import MockOXR


# Checks if today is a workday (Mon-Fri)
def is_work_day():
    today = date.today().weekday()
    return today < 5


# Checks if now is a workhour (9-19)
def is_work_hour():
    current_time = datetime.now().time()
    hour = current_time.hour
    return hour >= 9 and hour < 19


def get_last_day():
    weekend_threshold = get_weekend_threshold()
    last_day = (date.today() -
                timedelta(days=weekend_threshold)).strftime(DATE_FORMAT)
    return last_day


def get_weekend_threshold():
    today = date.today().weekday()
    if today == 6:  # Sunday
        return 2
    else:  # Saturday
        return 1


def percentage_diff(previous, current):
    try:
        percentage = round((abs(previous - current) / previous) * 100, 2)
    except ZeroDivisionError:
        percentage = float('inf')
    return percentage


class DolarStatusChecker:

    def __init__(self, threshold, use_mock_api, oxr_app_id) -> None:
        self.__api = MockOXR() if use_mock_api else OXR(oxr_app_id)
        self.__db = DB("data/historical_data.json")
        self.__threshold = threshold

    def check(self) -> str | None:
        # if not is_work_day() or not is_work_hour():
        #     print('Not working hour. Skipping')
        #     return

        # Flow
        # 1. Grab last day value from Database
        # 2. If not found, grab from API and store in Database
        # 3. Grab current value
        # 4. Store current value in another table
        last_day = get_last_day()
        last_value = self.__db.get_historical_data(last_day)
        if last_value is None:
            print('Cotação do dia anterior não encontrada, buscando na API...')
            res = self.__api.get_historical_data(last_day)
            last_value = res[VALUE_KEY]
            print(
                f'Cotação do dia anterior R${last_value}. Salvando localmente.'
            )
            self.__db.save_historical_data(date=last_day, value=last_value)

        last_stored_value = self.__db.get_last_stored_value()
        if last_stored_value is None:
            latest_data = self.__api.get_latest_data()
        else:
            existing_etag = last_stored_value[ETAG_KEY]
            existing_date_header = last_stored_value[DATE_HEADER_KEY]
            latest_data = self.__api.get_latest_data(existing_etag,
                                                     existing_date_header)

        etag = latest_data[ETAG_KEY]
        date_header = latest_data[DATE_HEADER_KEY]
        current_value = latest_data[VALUE_KEY]
        timestamp = latest_data[TIMESTAMP_KEY]
        self.__db.save_current_value(etag, date_header, timestamp,
                                     current_value)

        # Actual calculation
        diff = percentage_diff(last_value, current_value)
        diff_value = round(abs(last_value - current_value), 2)
        current_value_round = round(current_value, 2)
        if diff < self.__threshold:
            return f'Ainda não foi dessa vez. Cotação atual: R${current_value_round} - Variação: R${diff_value} ({diff}%)'

        print(
            f'Diff maior que {self.__threshold}%\n\tValor antigo: R${last_value}\n\tValor atual: R${current_value_round}\n\tDiff em R${diff_value}'
        )

        return f'Atenção! A cotação do dólar subiu em relação ao dia anterior! Cotação atual: R${current_value_round} - Variação: R${diff_value} ({diff}%)'
