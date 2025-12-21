from domain.message.request_message import RequestMessage
from domain.message.response_message import ResponseMessage


class MessagesManager:
    def __init__(self):
        self._data = {
            'recomend': {},
            'moderate': {}
        }
    
    def save(self, message: RequestMessage | ResponseMessage):
        self._data[message._command][message._tg_id] = message        
        
    def load(self, tg_id: int, command: str) -> RequestMessage | ResponseMessage | None:
        return self._data[command].get(tg_id, None)
    
    def clear(self, tg_id: int) -> None:
        del self._data['recomend'][tg_id]
        del self._data['moderate'][tg_id]
