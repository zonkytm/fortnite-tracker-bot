import logging
from aiogram import Bot, Dispatcher
from aiogram import executor
import handlers
import repository
import os

API_TOKEN = "7431069933:AAF_Vx9D18kI64uA49TxzSlcJA8Ecklgjkk"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def on_startup(dp):
    await repository.create_db()
    await handlers.register_handlers(dp, bot)
    await handlers.start_scheduler(dp)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
