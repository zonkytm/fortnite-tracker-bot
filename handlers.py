from datetime import datetime, timedelta
import subprocess

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import FileIsTooBig
import logging
import os
import command_list
import repository
import const
import aiohttp

async def send_weekly_message(dp):
    user_ids = await repository.get_all_users()
    for user_id in user_ids:
        try:
            await dp.bot.send_message(chat_id=user_id, text=const.ad_text)
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")


# Создаем и настраиваем планировщик
scheduler = AsyncIOScheduler()


async def start_scheduler(dp):
    start_time = datetime.now() + timedelta(minutes=1)
    scheduler.add_job(send_weekly_message, 'interval', days=1, args=[dp], start_date=start_time)
    scheduler.start()


async def start_command(message: types.Message):
    await repository.add_user(message.from_user.id)
    await message.answer(command_list.commands[command_list.Commands.start])
    await message.delete()

async def help_command(message: types.Message):
    await message.answer(command_list.commands[command_list.Commands.help])
    await message.delete()


async def delete_command(message: types.Message):
    await message.delete()


async def get_epic_stats(message: types.Message):
    try:
        # Извлекаем имя пользователя из команды
        command_args = message.get_args()
        if not command_args:
            await message.reply("Пожалуйста, укажите имя пользователя. Пример: /get_stats {username}")
            return

        username = command_args.strip()

        # Отправляем запрос к API с использованием имени пользователя
        url = f"https://fortnite-api.com/v2/stats/br/v2"
        headers = {
            "Authorization": "5df526ae-cb94-4f87-8281-c9f8a5397ba3"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params={"name": username, "image" : "all"}) as response:
                if response.status != 200:
                    await message.reply("Не удалось получить данные об аккаунте. Пожалуйста, проверьте имя пользователя.")
                    return

                data = await response.json()
                
                # Извлекаем необходимые данные
                account_info = data["data"]["account"]
                battle_pass = data["data"]["battlePass"]
                overall_stats = data["data"]["stats"]["all"]["overall"]

                # Формируем текст ответа
                response_text = command_list.commands[command_list.Commands.epic_stats].format(
                    account_name=account_info['name'],
                    account_id=account_info['id'],
                    battle_pass_level=battle_pass['level'],
                    battle_pass_progress=battle_pass['progress'],
                    score=overall_stats['score'],
                    wins=overall_stats['wins'],
                    kills=overall_stats['kills'],
                    matches=overall_stats['matches'],
                    win_rate=overall_stats['winRate']
                )

            if "image" in data["data"]:
                image_url = data["data"]["image"]
                await message.answer_photo(photo=image_url, caption=response_text)
            else:
                await message.answer(response_text)

    except Exception as e:
        await message.reply("Произошла ошибка при обработке запроса. Попробуйте снова.")
        print(f"Ошибка: {e}")

async def send_waiting_sticker(message: types.Message, bot) -> types.Message:
    # Отправка стикера с песочными часами
    try:
        # Попытка отправить стикер с песочными часами
        sticker_message = await message.reply("⌛")
        return sticker_message
    except Exception as e:
        # Обработка любых других исключений, чтобы избежать прерывания работы
        logging.error(f"Ошибка при отправке стикера: {e}")
        text_message = await message.reply("Ожидайте...")
        return text_message


async def remove_message(bot, message_id, chat_id):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logging.error(f"Ошибка при удалении сообщения: {e}")


async def register_handlers(dp: Dispatcher, bot):
    dp.register_message_handler(start_command, commands=[command_list.Commands.start.value])
    dp.register_message_handler(help_command, commands=[command_list.Commands.help.value])
    dp.register_message_handler(get_epic_stats, commands=[command_list.Commands.epic_stats.value])
    dp.register_message_handler(delete_command, content_types=types.ContentType.TEXT)

