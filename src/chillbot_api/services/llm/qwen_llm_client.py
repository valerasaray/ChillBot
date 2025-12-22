import requests
import json

from services.config.config import LlmConfig
from services.llm.abstract_llm_client import AbstractLlmClient
from services.logger.logger import logger


class QwenLlmClient(AbstractLlmClient):
    def __init__(self, config: LlmConfig):
        self._config = config
    
    def invoke(self, message: str) -> str:
        response = requests.post(
            url=self._config.url,
            headers={
                "Authorization": f"Bearer {self._config.api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": self._config.model,
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            })
        )
        
        logger.info(response)
        
        return response.text
    