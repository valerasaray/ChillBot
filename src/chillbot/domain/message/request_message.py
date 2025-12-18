from dataclasses import dataclass

from services.logger.logger import logger

@dataclass
class RequestMessage:
    _tg_id: str
    _request_params: dict
    _text: str | None = None
    _command: str | None = None
    _context: str | None = None
    
    def as_dict(self) -> dict:
        return {
            'tg_id': self._tg_id,
            'text': self._text,
            'commmand': self._command,
            'context': self._context,
            'request_params': self._request_params
        }

    def update_context(self, context: str) -> None:
        logger.info(self._command)
        logger.info(self._context)
        if self._command is None:
            if self._context is None:
                self._context = f'- {context}\n'
                return

            self._context += f'- {context}\n'
        logger.info(self._command)
        logger.info(self._context)
        
        
    def clear_context(self):
        self._context = None
    