from dataclasses import dataclass


@dataclass
class RequestMessage:
    _tg_id: str
    _text: str | None = None
    _command: str | None = None
    _context: str | None = None
    
    def as_dict(self) -> dict:
        return {
            'tg_id': self._tg_id,
            'text': self._text,
            'commmand': self._command,
            'context': self._context
        }

    @staticmethod
    def from_dict(d: dict) -> 'RequestMessage':
        return RequestMessage(
            _tg_id=d['tg_id'],
            _text=d.get('text', None),
            _command=d.get('command', None),
            _context=d.get('context', None)
        )
        