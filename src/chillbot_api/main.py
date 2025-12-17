import asyncio

from services.config.config import Config
from services.kafka.consumer import Consumer
from services.logger.logger import logger
from services.llm.qwen_llm_client import QwenLlmClient
from services.postgres.session import PostgresSession
from services.postgres.repositories.postgres_comment_repository import PostgresCommentRepository
from services.postgres.repositories.postgres_place_repository import PostgresPlaceRepository
from services.postgres.repositories.postgres_rate_repository import PostgresRateRepository
from services.postgres.repositories.postgres_user_repository import PostgresUserRepository
from usecases.messages_processor.messages_processor import MessagesProcessor


async def main():
    config = Config.from_env()
    
    consumer = Consumer(config.kafka)
    
    llm_client = QwenLlmClient(config.llm)
    
    postgres_session = PostgresSession(config.database)
    comment_repository = PostgresCommentRepository(postgres_session)
    user_repository = PostgresUserRepository(postgres_session)
    place_repository = PostgresPlaceRepository(postgres_session)
    rate_repository = PostgresRateRepository(postgres_session)
    
    processor = MessagesProcessor(
        llm_client,
        comment_repository,
        user_repository,
        place_repository,
        rate_repository
    )
    
    for message in consumer.listen():
        try:
            logger.info(f'received message: {message}')
            await processor.process(message)
        except Exception as e:
            logger.error(e)
            continue


if __name__ == '__main__':
    asyncio.run(main())
