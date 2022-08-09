from dotenv import load_dotenv
from dolar_bot import DolarBot

load_dotenv()

bot = DolarBot(
    threshold=5, # Porcentagem de aumento
    mock_api=True # Avoid calling real API for testing
)
bot.watch()