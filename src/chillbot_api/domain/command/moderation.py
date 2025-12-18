from pydantic import BaseModel
from domain.message.request_message import RequestMessage
from domain.message.response_message import ResponseMessage


class ModerationRequestCommand(BaseModel):
    prev_comment_id: int | None
    accept: bool | None
    tg_id: str
    place_offset: int

    @staticmethod
    def from_mesage(message: RequestMessage) -> 'ModerationRequestCommand':
        return ModerationRequestCommand(
            tg_id=message._tg_id
        )


class ModerationResponse(BaseModel):
    tg_id: str
    user: str
    text: str
    rate: int
    place: str
    comment_id: int
    place_offset: int

    def to_mesage(self) -> 'ResponseMessage':
        return ResponseMessage(
            _tg_id=self.tg_id,
            _command='moderation',
            _text=self.text,
            _response_params={
                'success': True,
                'comment_id': self.comment_id,
                'rate': self.rate,
                'place': self.place,
                'user': self.user,
                'place_offset': self.place_offset
            }
        )
    