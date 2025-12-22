import os
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from services.user_data import UserDataManager
from domain.message.request_message import RequestMessage
from domain.message.response_message import ResponseMessage
from domain.city.cities_list import cities_list
from domain.categories.categories_list import categories_list
from services.config.config import Config
from services.kafka.consumer import Consumer
from services.kafka.producer import Producer
from services.logger.logger import logger
from usecases.messages_manager.messages_manager import MessagesManager


class Comment(StatesGroup):
    city = State()
    category = State()
    place = State()
    rating = State()
    comment = State()


dp = Dispatcher(storage=MemoryStorage())

user_manager = UserDataManager()


@dp.message(Command("start"))
async def handle_start(message: Message, kafka_producer: Producer, config: Config):
    id = message.from_user.id
    
    user_create_request = RequestMessage(
        _command='user_create',
        _tg_id=id,
        _request_params={'is_admin': int(id) in config.bot.admin_ids}
    )
    
    kafka_producer.produce(user_create_request.as_dict())


@dp.message(Command("comment"))
async def post_comment(message: Message, state: FSMContext):
    await state.set_state(Comment.city)
    cities = '\n' + '\n'.join(sorted(cities_list))
    await message.answer(f"Выберите город из списка: {cities}")
    
    
@dp.message(Comment.city)
async def post_comment_2(message: Message, state: FSMContext):
    if message.text in cities_list:
        await state.update_data(city=message.text)
        await state.set_state(Comment.category)
        categories = '\n' + '\n'.join(sorted(categories_list))
        await message.answer(f"Выберите категорию из списка: {categories}")
    else:
        await message.answer('Неправильный город, попробуйте еще раз')
    

@dp.message(Comment.category)
async def post_comment_3(message: Message, state: FSMContext):
    if message.text in categories_list:
        await state.update_data(category=message.text.lower())
        await state.set_state(Comment.place)
        await message.answer(f'Введите место:')
    else:
        await message.answer('Неправильная категория, попробуйте еще раз')

@dp.message(Comment.place)
async def post_comment_4(message: Message, state: FSMContext):
    await state.update_data(place=message.text)
    await state.set_state(Comment.rating)
    await message.answer("Оцените место (от 1 до 5):")


@dp.message(Comment.rating)
async def post_comment_5(message: Message, state: FSMContext):
    await state.update_data(rating=message.text)
    await state.set_state(Comment.comment)
    await message.answer("Оставьте отзыв:")


@dp.message(Comment.comment)
async def post_comment_final(message: Message, state: FSMContext, kafka_producer: Producer):
    id = message.from_user.id
    await state.update_data(comment=message.text)
    data = await state.get_data()
    try:
        request = RequestMessage(
            _tg_id=id,
            _command='comment',
            _text=data['comment'],
            _request_params={
                'place_name': data['place'],
                'rate': int(data['rating'])
            }
        )
        kafka_producer.produce(request.as_dict())
    finally:
        await state.clear()


@dp.message(Command("moderate"))
async def moderate(message: Message, kafka_producer: Producer):
    id = message.from_user.id
    try:
        request = RequestMessage(
            _tg_id=id,
            _command='moderate',
            _text='',
            _request_params={
                'accept': None,
                'place_offset': 0,
                'prev_comment_id': None
            }
        )
        kafka_producer.produce(request.as_dict())
    finally:
        pass


@dp.message(Command('accept'))
async def accept(message: Message, kafka_producer: Producer, messages_manager: MessagesManager):
    id = message.from_user.id
    comment = messages_manager.load(id, 'moderate')
    logger.info(comment)
    try:
        request = RequestMessage(
            _tg_id=id,
            _command='moderate',
            _text='',
            _request_params={
                'accept': True,
                'place_offset': comment._response_params['place_offset'],
                'prev_comment_id': comment._response_params['comment_id']
            }
        )
        kafka_producer.produce(request.as_dict())
    finally:
        pass

@dp.message(Command('decline'))
async def accept(message: Message, kafka_producer: Producer, messages_manager: MessagesManager):
    id = message.from_user.id
    comment = messages_manager.load(id, 'moderate')
    logger.info(comment)
    try:
        request = RequestMessage(
            _tg_id=id,
            _command='moderate',
            _text='',
            _request_params={
                'accept': False,
                'place_offset': comment._response_params['place_offset'],
                'prev_comment_id': comment._response_params['comment_id']
            }
        )
        kafka_producer.produce(request.as_dict())
    finally:
        pass

@dp.message()
async def handle_with_manager(message: Message, kafka_producer: Producer, messages_manager: MessagesManager):
    id = message.from_user.id
    text = message.text
    
    old_message = messages_manager.load(id, 'recomend')
    
    message = RequestMessage(
        _command='recomend',
        _text=text,
        _context=old_message._context if old_message is not None else None,
        _tg_id=id,
        _request_params={
            'success': old_message._request_params['success'] if old_message is not None else None,
            'category': old_message._request_params['category'] if old_message is not None else None,
            'city': old_message._request_params['city'] if old_message is not None else None,
            'comments': old_message._request_params['comments'] if old_message is not None else None,
        }
    )
    
    if old_message is not None and old_message._context is not None:
        for item in old_message._context.strip('\n').split('\n'):
            message.update_context(context=item.strip(' -'))
    message.update_context(context=text)
    
    messages_manager.save(message)
    
    kafka_producer.produce(
        message=message.as_dict()
    )


async def listen_kafka(kafka_consumer: Consumer, messages_manager: MessagesManager, bot: Bot):
    async for message_dict in kafka_consumer.listen():
        try:
            logger.info(f"Received message: {message_dict}")
            response_message = ResponseMessage.from_dict(message_dict)
            logger.info(f"Received message: {response_message}")
            if response_message._command == 'recomend':
                logger.info(response_message._response_params['success'])
                request_message = messages_manager.load(response_message._tg_id, response_message._command)
                if request_message is not None and request_message._command == 'recomend':
                    if response_message._response_params['success']:
                        logger.info('IUGHFIUWGFOIUWEGHFIOWUEGHFOEWIUHF')
                        messages_manager.clear(response_message._tg_id, 'recomend')
                    elif not response_message._response_params['success'] and response_message._response_params['fatal']:
                        logger.info('IUGHFIUWGFOIUWEGHFIOWUEGHFOEWIUHF 2')
                        messages_manager.clear(response_message._tg_id, 'recomend')
                    else:
                        logger.info('IUGHFIUWGFOIUWEGHFIOWUEGHFOEWIUHF 3')
                        request_message.update_context(response_message._text)
                        messages_manager.save(request_message)
            elif response_message._command == 'moderate' and response_message._response_params['success']:
                logger.info(response_message)
                messages_manager.save(response_message)
            logger.info(response_message)
            
            await response_message.send_to_user(bot)
        except Exception as ex:
            logger.exception(f"Error processing message: {ex.with_traceback()}")


async def main():
    config = Config.from_env()
    
    bot = Bot(token=config.bot.token)
    
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
    kafka_task = asyncio.create_task(listen_kafka(kafka_consumer, messages_manager, bot))
    
    try:
        await asyncio.gather(server_task, kafka_task)
    finally:
        server_task.cancel()
        kafka_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
