from abc import ABC, abstractmethod
from domain.llm.message import LlmMessage
from typing import Type


class AbstractLlmClient(ABC):
    @abstractmethod
    def invoke(self, prompt: str, message: Type[LlmMessage]) -> LlmMessage:
        pass
    