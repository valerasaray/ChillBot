from typing import Any

from domain.message.request_message import RequestMessage
from services.logger.logger import logger
from services.repositories.abstract_comment_repository import AbstractCommentRepository
from services.repositories.abstract_place_repository import AbstractPlaceRepository
from services.repositories.abstract_user_repository import AbstractUserRepository
from services.repositories.abstract_rate_repository import AbstractRateRepository
from services.kafka.producer import Producer
from services.llm.abstract_llm_client import AbstractLlmClient


class MessagesProcessor:
    def __init__(
        self,
        kafka_producer: Producer,
        llm_client: AbstractLlmClient,
        comment_repository: AbstractCommentRepository,
        user_repository: AbstractUserRepository,
        place_repository: AbstractPlaceRepository,
        rate_repository: AbstractRateRepository
    ):
        self._kafka_producer = kafka_producer
        self._llm_client = llm_client
        self._comment_repository = comment_repository
        self._user_repository = user_repository
        self._place_repository = place_repository
        self._rate_repository = rate_repository
    
    async def process(self, message_dict: dict) -> Any:
        logger.info(message_dict)
        message = RequestMessage.from_dict(message_dict)
        message._text += '1'
        self._kafka_producer.produce(message.as_dict())
