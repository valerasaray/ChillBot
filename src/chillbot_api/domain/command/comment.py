from pydantic import BaseModel
from domain.message.request_message import RequestMessage


class CommentCommand(BaseModel):
    text: str
    rate: int
    place_name: str

    @staticmethod
    def from_mesage(message: RequestMessage) -> 'CommentCommand':
        return CommentCommand(
            text=message._text,
            place_name=message._request_params['place_name'],
            rate=message._request_params['rate'],
        )
    