from time import time

import telegram
from constants import DATE_FORMAT, VALUE_KEY, DATE_KEY
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
        percentage = (abs(previous - current) / previous) * 100
    except ZeroDivisionError:
        percentage = float('inf')
    return percentage


class DolarBot:

    def __init__(self, threshold, use_mock_api, oxr_app_id, telegram_token,
                 telegram_chat_id) -> None:
        self.__api = MockOXR() if use_mock_api else OXR(oxr_app_id)
        self.__db = DB("data/historical_data.json")
        self.__threshold = threshold
        self.__bot = telegram.Bot(token=telegram_token)
        self.__chat_id = telegram_chat_id

    async def check(self) -> None:
        if not is_work_day() or not is_work_hour():
            print('Not working hour. Skipping')
            return

        last_rate = self.__db.get_last_stored_value()
        print("Utilizando última cotação armazenada. Valor: R$" +
              str(last_rate))

        if last_rate is None:
            print("Buscando cotação do dia anterior.")
            # Busca do dia anterior
            last_day = get_last_day()
            api_res = self.__api.get_historical_data(last_day)
            last_rate = api_res[VALUE_KEY]
            print("Cotação anterior: R$" + str(last_rate))
            self.__db.store_historical_data(date=time(), value=last_rate)

        current_api_res = self.__api.get_latest_data()
        current_value = current_api_res[VALUE_KEY]
        self.__db.store_historical_data(date=time(), value=current_value)

        diff = percentage_diff(last_rate, current_value)
        if diff > self.__threshold:
            print("Diff maior que " + str(self.__threshold) +
                  "% \n\tValor antigo: R$" + str(last_rate) +
                  "\n\tValor atual: R$" + str(current_value) +
                  "\n\tDiff em R$" + str(abs(last_rate - current_value)))

            message = f'Atenção! A cotação do dólar subiu {diff}%!'

            await self.__bot.send_message(chat_id=self.__chat_id, text=message)
        else:
            print("Não foi dessa vez - Diff = " + str(diff) +
                  " Valor Atual = " + str(current_value))
