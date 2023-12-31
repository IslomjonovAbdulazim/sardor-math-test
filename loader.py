from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils.db_api.results import Results
from utils.db_api.sqlite import Database
from data import config
from utils.db_api.test import DatabaseTest

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(path_to_db="data/main.db")
test = DatabaseTest(path_to_db="data/test.db")
results = Results(path_to_db="data/results.db")
