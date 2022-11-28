from config import TELEGRAM_BOT_TOKEN
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


