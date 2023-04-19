import os
from dotenv import load_dotenv
from dolar_status_checker import DolarStatusChecker
from telegram.ext import Application, CallbackContext

load_dotenv()

def get_int_from_env(env_name, default_value=None):
    env_var_value = os.getenv(env_name, default=default_value)
    if env_var_value is None or not env_var_value.isdigit():
        raise ValueError(f"Environment variable '{env_name}' is not present or not a numeric value.")

    return int(env_var_value)

use_mock_api = os.getenv('USE_MOCK_OXR_API', 'False').lower() in ('true', '1')
oxr_app_id = os.getenv('OXR_APP_ID')
telegram_token = os.getenv('TELEGRAM_TOKEN', '')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
interval_minutes = get_int_from_env('RUN_INTERVAL', '25')
diff_threshold = get_int_from_env('DIFF_THRESHOLD', '1')

bot = DolarStatusChecker(
    threshold=diff_threshold,  # Porcentagem de aumento
    use_mock_api=use_mock_api,  # Avoid calling real API for testing
    oxr_app_id=oxr_app_id)

async def check_status(context: CallbackContext):
    result = bot.check()
    if result is not None:
        await context.bot.send_message(chat_id=telegram_chat_id, text=result)

def main():
    application = Application.builder().token(telegram_token).build()

    if application.job_queue is not None:
        application.job_queue.run_repeating(check_status, interval=60 * interval_minutes, first=0)

    application.run_polling()


if __name__ == '__main__':
    main()