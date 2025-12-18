from abc import ABC


class AbstractBot(ABC):
    async def send_message(self, chat_id: str, message: str) -> None:
        pass
