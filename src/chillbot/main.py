import os
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from services.user_data import UserDataManager

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [
    int(id_str.strip())
    for id_str in os.getenv("ADMIN_IDS").split(",")
    if id_str.strip()
]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_manager = UserDataManager()


@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет!")


@dp.message(Command("admin"))
async def handle_admin_allowed(message: Message):
    user_id = message.from_user.id

    if user_id not in ADMIN_IDS:
        await message.answer("У вас нет прав доступа к этой команде!")
        return

    await message.answer("Вы вошли в админ-панель. Доступ разрешен.")


@dp.message(Command("last"))
async def show_last_message(message: Message):
    user_id = message.from_user.id
    last_msg = user_manager.get_last_message(user_id)

    if last_msg:
        await message.answer(
            f"Ваше последнее сообщение:\n"
            f"Текст: {last_msg['text']}\n"
            f"Время: {last_msg['timestamp']}"
        )
    else:
        await message.answer("У вас нет сохраненных сообщений")


@dp.message()
async def handle_with_manager(message: Message):
    user_id = message.from_user.id
    text = message.text

    user_manager.save_message(user_id, text)

    await message.answer(f"Сохранил ваше сообщение: '{text}'")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
