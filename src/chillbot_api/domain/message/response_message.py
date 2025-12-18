from dataclasses import dataclass


@dataclass
class ResponseMessage:
    _tg_id: str
    _response_params: dict
    _text: str | None = None
    _command: str | None = None
    _context: str | None = None
        
    @staticmethod
    def from_dict(d: dict) -> 'ResponseMessage':
        return ResponseMessage(
            _tg_id=d['tg_id'],
            _text=d.get('text', None),
            _command=d.get('command', None),
            _context=d.get('context', None),
            _response_params=d.get('response_params', {})
        )
