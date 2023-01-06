from config import TELEGRAM_BOT_TOKEN
import asyncio
import logging
from aiogram import Bot, Dispatcher

from handlers.hiring.hiring import router as router_hiring
from handlers.summary.summary import router as router_summary

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def main():

    dp.include_router(router_hiring)
    dp.include_router(router_summary)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
