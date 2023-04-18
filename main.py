import asyncio
import os
from dotenv import load_dotenv
import schedule
from dolar_bot import DolarBot

load_dotenv()

use_scheduler = os.getenv('USE_SCHEDULER', 'False').lower() in ('true', '1')
use_mock_api = os.getenv('USE_MOCK_OXR_API', 'False').lower() in ('true', '1')
oxr_app_id = os.getenv('OXR_APP_ID')
telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

bot = DolarBot(
    threshold=5,  # Porcentagem de aumento
    use_mock_api=use_mock_api,  # Avoid calling real API for testing
    oxr_app_id=oxr_app_id,
    telegram_token=telegram_token,
    telegram_chat_id=telegram_chat_id)


async def main():
    if use_scheduler:
        print('Using scheduler. Running every 10 minutes during work days.')

        while True:
            # Sleep
            await asyncio.sleep(60 * 1)
            # Executa a task
            await bot.check()
    else:
        print('Single time check.')
        await bot.check()


if __name__ == '__main__':
    asyncio.run(main())