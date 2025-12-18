from aiogram import Bot

from domain.bot.abstract_bot import AbstractBot

class AiogramBot(AbstractBot):
    def __init__(self, bot_instance: Bot):
        self._bot_instance: Bot = bot_instance
        
    def send_message(self, chat_id: str, message: str) -> None:
        self._bot_instance.send_message(
            chat_id=chat_id,
            message=message
        )
