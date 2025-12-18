from usecases.command.abstract_command import AbstractCommand
from domain.command.create_user import CreateUserCommand
from domain.message.request_message import RequestMessage
from domain.message.response_message import ResponseMessage
from services.repositories.abstract_user_repository import AbstractUserRepository


class UserCreate(AbstractCommand):
    def __init__(self, user_repository: AbstractUserRepository):
        self._user_repository = user_repository
        
    async def run(self, request: RequestMessage) -> ResponseMessage:
        command = CreateUserCommand.from_mesage(request)
        
        user_records = await self._user_repository.list(
            tg_id=command.tg_id
        )
        
        if len(user_records) == 0:
            await self._user_repository.create(
                is_admin=command.is_admin,
                tg_id=command.tg_id
            )

        text_common = 'Добрый день, Вы можете спросить у меня про места отдыха в вашем городе, а также оставить свой отзыв об этих местах.'
        text_moder = '\nВам присвоена роль admin. Вы можете при помощи команды /moderate удалять или подтверждать отзывы пользователей.'
            
        return ResponseMessage(
            _tg_id=request._tg_id,
            _response_params={
                'success': True
            },
            _text=f'{text_common}{text_moder if command.is_admin else ""}',
        )
    