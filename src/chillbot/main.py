import os
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from services.user_data import UserDataManager
from domain.message.request_message import RequestMessage
from domain.message.response_message import ResponseMessage
from services.config.config import Config
from services.kafka.consumer import Consumer
from services.kafka.producer import Producer
from services.logger.logger import logger
from usecases.messages_manager.messages_manager import MessagesManager


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [
    int(id_str.strip())
    for id_str in os.getenv("ADMIN_IDS").split(",")
    if id_str.strip()
]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

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


@dp.message()
async def handle_with_manager(message: Message, kafka_producer: Producer, messages_manager: MessagesManager):
    id = message.from_user.id
    text = message.text
    
    message = RequestMessage(
        _text=text,
        _tg_id=id,
        _request_params={}
    )
    old_message = messages_manager.load(id)
    if old_message is not None and old_message._context is not None:
        for item in old_message._context.strip('\n').split('\n'):
            message.update_context(context=item.strip(' -'))
    message.update_context(context=text)
    
    messages_manager.save(message)
    
    kafka_producer.produce(
        message=message.as_dict()
    )


async def listen_kafka(kafka_consumer: Consumer, messages_manager: MessagesManager):
    async for message_dict in kafka_consumer.listen():
        try:
            logger.debug(f"Received message: {message_dict}")
            response_message = ResponseMessage.from_dict(message_dict)
            
            request_message = messages_manager.load(response_message._tg_id)
            request_message.update_context(response_message._text)
            messages_manager.save(request_message)
            
            await response_message.send_to_user(bot)
        except Exception as ex:
            logger.exception(f"Error processing message: {ex.with_traceback()}")


async def main():
    config = Config.from_env()
    kafka_consumer = Consumer(
        config=config.kafka_conmsumer
    )
    kafka_producer = Producer(
        config=config.kafka_producer
    )
    
    messages_manager = MessagesManager()
    
    dp.workflow_data['config'] = config
    dp.workflow_data["kafka_producer"] = kafka_producer
    dp.workflow_data['messages_manager'] = messages_manager
    
    server_task = asyncio.create_task(dp.start_polling(bot))
    kafka_task = asyncio.create_task(listen_kafka(kafka_consumer, messages_manager))
    
    try:
        await asyncio.gather(server_task, kafka_task)
    finally:
        server_task.cancel()
        kafka_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
