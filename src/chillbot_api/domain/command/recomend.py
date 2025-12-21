from pydantic import BaseModel
from domain.message.request_message import RequestMessage
from domain.message.response_message import ResponseMessage


class RecomendComment(BaseModel):
    text: str
    rate: int
    
    def key(self):
        return self.rate


class RecomendCommand(BaseModel):
    tg_id: int
    message: str
    context: str
    city: str | None
    category: str | None
    comments: dict[str, list[RecomendComment]] | None
    success: bool
    
    @staticmethod
    def from_message(message: RequestMessage) -> 'RecomendCommand':
        return RecomendCommand(
            message=message._text,
            success=bool(message._request_params['success']),
            category=message._request_params['category'],
            comments=message._request_params['comments'],
            city=message._request_params['city'],
            context=message._context,
            tg_id=message._tg_id
        )
    