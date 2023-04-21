from time import time
from zoneinfo import ZoneInfo

from constants import DATE_FORMAT, DATE_HEADER_KEY, ETAG_KEY, TIMESTAMP_KEY, VALUE_KEY, DATE_KEY
from database import DB
from datetime import date, datetime, timedelta
from oxr import OXR
from mock_oxr import MockOXR
from logging import getLogger

logger = getLogger(__name__)

timezone = ZoneInfo(key="America/Sao_Paulo")

# Checks if today is a workday (Mon-Fri)
def is_work_day(weekday):
    return weekday < 5

# Checks if now is a workhour (9-19)
def is_work_hour(hour):
    return hour >= 9 and hour < 19


def get_last_day(now: datetime):
    weekend_threshold = get_weekend_threshold(now.date().weekday())
    last_day = (now.date() -
                timedelta(days=weekend_threshold)).strftime(DATE_FORMAT)
    return last_day


def get_weekend_threshold(weekday):
    if weekday == 6:  # Sunday
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
        now = datetime.now(tz=timezone)
        if not is_work_day(now.date().weekday()) or not is_work_hour(now.time().hour):
            logger.info('Not a working hour. Skipping execution.')
            return

        last_day = get_last_day(now)
        last_day_value = self.__db.get_historical_data(last_day)

        if last_day_value is None:
            logger.info(
                'Cotação do dia anterior não encontrada, buscando na API...')
            res = self.__api.get_historical_data(last_day)
            last_day_value = res[VALUE_KEY]
            logger.info('Cotação do dia anterior R$%f. Salvando localmente.',
                        last_day_value)
            self.__db.save_historical_data(date=last_day, value=last_day_value)

        last_stored_value = self.__db.get_last_stored_value()
        if last_stored_value is None:
            logger.info('Sem dados armazenados, buscando da API...')
            latest_data = self.__api.get_latest_data()
        else:
            existing_etag = last_stored_value[ETAG_KEY]
            existing_date_header = last_stored_value[DATE_HEADER_KEY]
            latest_data = self.__api.get_latest_data(existing_etag,
                                                     existing_date_header)
            if existing_etag == latest_data[ETAG_KEY] or last_stored_value[
                    VALUE_KEY] == latest_data[VALUE_KEY]:
                logger.info(
                    'Sem modificação no ETag ou Cotação anterior. Ignorando execução.'
                )
                return

        etag = latest_data[ETAG_KEY]
        date_header = latest_data[DATE_HEADER_KEY]
        current_value = latest_data[VALUE_KEY]
        timestamp = latest_data[TIMESTAMP_KEY]
        self.__db.save_current_value(etag, date_header, timestamp,
                                     current_value)

        # Actual calculation
        diff = percentage_diff(last_day_value, current_value)
        diff_value = round(abs(last_day_value - current_value), 2)
        current_value_round = round(current_value, 2)
        if diff < self.__threshold:
            return f'Ainda não foi dessa vez. Cotação atual: R${current_value_round} - Variação: R${diff_value} ({diff}%)'

        logger.info(
            'Diferença maior que o threshold configurado de %f%. Valor do dia anterior: R$%f - Valor atual: R$%f - Diferença em R$%f',
            self.__threshold, last_day_value, current_value_round, diff_value)

        return f'Atenção! A cotação do dólar subiu em relação ao dia anterior! Cotação do dia anterior: R${last_day_value}. Cotação atual: R${current_value_round} - Variação: R${diff_value} ({diff}%)'
