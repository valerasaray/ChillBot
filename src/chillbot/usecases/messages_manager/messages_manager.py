from domain.message.request_message import RequestMessage


class MessagesManager:
    def __init__(self):
        self._data = {}
    
    def save(self, message: RequestMessage):
        self._data[message._tg_id] = message        
        
    def load(self, tg_id: str) -> RequestMessage | None:
        return self._data.get(tg_id, None)
    
    def clear(self, tg_id: str) -> None:
        del self._data[tg_id]
