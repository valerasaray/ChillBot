import json
import time
import asyncio
from aiokafka import AIOKafkaConsumer

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaError
from services.logger.logger import logger
from services.config.config import KafkaConfig


class Consumer:
    def __init__(self, config: KafkaConfig):
        self._config: KafkaConfig = config
        self._consumer = self._connect()
    
    async def _connect(self):
        while True:
            try:
                logger.info(f"Connecting to Kafka {self._config.host}:{self._config.port}...")
                self._consumer = AIOKafkaConsumer(
                    self._config.topic,
                    bootstrap_servers=f'{self._config.host}:{self._config.port}',
                    auto_offset_reset=self._config.auto_offset_reset,
                    enable_auto_commit=self._config.enable_auto_commit,
                    group_id=self._config.group_id
                )
                await self._consumer.start()
                logger.info("Connected to Kafka")
                return
            except KafkaError:
                logger.warning(f"Kafka not available. Retrying in {self._config.initial_timeout} sec...")
                await asyncio.sleep(self._config.initial_timeout)

    async def listen(self):
        await self._connect()
        try:
            async for message in self._consumer:
                yield json.loads(message.value.decode())
        finally:
            await self._consumer.stop()
    