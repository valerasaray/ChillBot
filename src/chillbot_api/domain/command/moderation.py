from pydantic import BaseModel
from domain.message.request_message import RequestMessage
from domain.message.response_message import ResponseMessage


class ModerationRequestCommand(BaseModel):
    prev_comment_id: int | None
    accept: bool | None
    tg_id: int
    place_offset: int

    @staticmethod
    def from_mesage(message: RequestMessage) -> 'ModerationRequestCommand':
        return ModerationRequestCommand(
            tg_id=message._tg_id,
            accept=bool(message._request_params['accept']) if message._request_params['accept'] is not None else None,
            place_offset=int(message._request_params['place_offset']),
            prev_comment_id=int(message._request_params['prev_comment_id']) if message._request_params['prev_comment_id'] is not None else None
        )


class ModerationResponse(BaseModel):
    tg_id: int
    user: int
    text: str
    rate: int
    place: str
    city: str
    category: str
    comment_id: int
    place_offset: int

    def to_mesage(self) -> 'ResponseMessage':
        return ResponseMessage(
            _tg_id=self.tg_id,
            _command='moderate',
            _text=f'Пользователь {self.user} оставил комментарий к месту {self.place} (город {self.city}, категрия {self.category}). Рейтинг: {self.rate}, текст: {self.text}',
            _response_params={
                'success': True,
                'comment_id': self.comment_id,
                'rate': self.rate,
                'place': self.place,
                'user': self.user,
                'place_offset': self.place_offset
            }
        )
