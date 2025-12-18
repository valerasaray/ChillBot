from abc import ABC, abstractmethod


class AbstractLlmClient(ABC):
    @abstractmethod
    def invoke(self, message: str) -> str:
        pass
    