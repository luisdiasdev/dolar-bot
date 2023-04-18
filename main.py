import asyncio
import os
from dotenv import load_dotenv
import schedule
from dolar_status_checker import DolarStatusChecker
from telegram.ext import Application, CallbackContext

load_dotenv()

use_scheduler = os.getenv('USE_SCHEDULER', 'False').lower() in ('true', '1')
use_mock_api = os.getenv('USE_MOCK_OXR_API', 'False').lower() in ('true', '1')
oxr_app_id = os.getenv('OXR_APP_ID')
telegram_token = os.getenv('TELEGRAM_TOKEN', '')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

bot = DolarStatusChecker(
    threshold=5,  # Porcentagem de aumento
    use_mock_api=use_mock_api,  # Avoid calling real API for testing
    oxr_app_id=oxr_app_id)

async def check_status(context: CallbackContext):
    result = bot.check()
    if result is not None:
        await context.bot.send_message(chat_id=telegram_chat_id, text=result)

def main():
    application = Application.builder().token(telegram_token).build()

    if application.job_queue is not None:
        application.job_queue.run_repeating(check_status, interval=60, first=0)

    application.run_polling()

    # if use_scheduler:
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete
    #     print('Using scheduler. Running every 10 minutes during work days.')

    #     while True:
    #         # Sleep
    #         await asyncio.sleep(60 * 1)
    #         # Executa a task
    #         await bot.check()
    # else:
    #     print('Single time check.')
    #     await bot.check()


if __name__ == '__main__':
    main()