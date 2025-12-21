from dataclasses import dataclass


@dataclass
class ResponseMessage:
    _tg_id: int
    _response_params: dict
    _text: str | None = None
    _command: str | None = None
    _context: str | None = None
    
    def as_dict(self) -> dict:
        return {
            'tg_id': self._tg_id,
            'text': self._text,
            'command': self._command,
            'context': self._context,
            'response_params': self._response_params
        }
    
    @staticmethod
    def from_dict(d: dict) -> 'ResponseMessage':
        return ResponseMessage(
            _tg_id=d['tg_id'],
            _text=d.get('text', None),
            _command=d.get('command', None),
            _context=d.get('context', None),
            _response_params=d.get('response_params', {})
        )
