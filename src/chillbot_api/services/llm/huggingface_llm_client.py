from huggingface_hub import InferenceClient
import json
from typing import Type
from domain.llm.message import LlmMessage
from services.config.config import LlmConfig
from services.llm.abstract_llm_client import AbstractLlmClient
from services.logger.logger import logger


class HuggingfaceLlmClient(AbstractLlmClient):
    def __init__(self, config: LlmConfig):
        self._config = config
    
    def invoke(self, prompt: str, message: Type[LlmMessage]) -> LlmMessage:
        client = InferenceClient(
            api_key=self._config.api_key,
        )

        completion = client.chat.completions.create(
            model=self._config.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                    ]
                }
            ],
        )
        data = completion.choices[0].message.content.strip(' \n`\t\r').replace('json', '')
        
        data_json = json.loads(data)
        logger.info(data_json)
        
        return message.from_json(data=data)
    