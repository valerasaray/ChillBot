from typing import Any

from domain.message.request_message import RequestMessage
from services.logger.logger import logger
from services.repositories.abstract_comment_repository import AbstractCommentRepository
from services.repositories.abstract_place_repository import AbstractPlaceRepository
from services.repositories.abstract_user_repository import AbstractUserRepository
from services.repositories.abstract_rate_repository import AbstractRateRepository
from services.kafka.producer import Producer
from services.llm.abstract_llm_client import AbstractLlmClient
from usecases.command.abstract_command import AbstractCommand
from usecases.command.comment import Comment
from usecases.command.moderation import Moderation
from usecases.command.user_create import UserCreate


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
        
        self._commands: dict[str, AbstractCommand] = {
            'user_create': UserCreate(
                user_repository=user_repository
            ),
            'comment': Comment(
                user_repository=user_repository,
                comment_repository=comment_repository,
                place_repository=place_repository,
                rate_repository=rate_repository
            ),
            'moderate': Moderation(
                rate_repository=rate_repository,
                comment_repository=comment_repository,
                place_repository=place_repository,
                user_repository=user_repository
            )
        }
    
    async def process(self, message_dict: dict) -> Any:
        logger.info(message_dict)
        message = RequestMessage.from_dict(message_dict)
        command = self._commands[message._command]
        response = await command.run(message)
        logger.info(response.as_dict())
        self._kafka_producer.produce(response.as_dict())
