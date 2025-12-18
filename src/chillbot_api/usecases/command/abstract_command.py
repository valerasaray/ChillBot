from abc import ABC, abstractmethod

from domain.message.request_message import RequestMessage
from domain.message.response_message import ResponseMessage


class AbstractCommand(ABC):
    @abstractmethod
    def run(self, request: RequestMessage) -> ResponseMessage:
        pass
