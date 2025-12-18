from dataclasses import dataclass

from domain.bot.abstract_bot import AbstractBot


@dataclass
class ResponseMessage:
    _tg_id: str
    _text: str | None = None
    _command: str | None = None
    _context: str | None = None
        
    @staticmethod
    def from_dict(d: dict) -> 'ResponseMessage':
        return ResponseMessage(
            _tg_id=d['tg_id'],
            _text=d.get('text', None),
            _command=d.get('command', None),
            _context=d.get('context', None)
        )

    async def send_to_user(self, bot: AbstractBot) -> None:
        await bot.send_message(
            chat_id=self._tg_id,
            text=self._text
        )
    