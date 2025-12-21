from pydantic import BaseModel
from domain.message.request_message import RequestMessage


class CreateUserCommand(BaseModel):
    tg_id: int
    is_admin: bool

    @staticmethod
    def from_mesage(message: RequestMessage) -> 'CreateUserCommand':
        return CreateUserCommand(
            is_admin=message._request_params['is_admin'],
            tg_id=message._tg_id
        )
    