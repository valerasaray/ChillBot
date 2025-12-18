from domain.command.moderation import ModerationRequestCommand, ModerationResponse
from domain.message.request_message import RequestMessage
from domain.message.response_message import ResponseMessage
from services.repositories.abstract_user_repository import AbstractUserRepository
from services.repositories.abstract_comment_repository import AbstractCommentRepository
from services.repositories.abstract_place_repository import AbstractPlaceRepository
from services.repositories.abstract_rate_repository import AbstractRateRepository
from usecases.command.abstract_command import AbstractCommand


class Moderation(AbstractCommand):
    def __init__(
        self, 
        comment_repository: AbstractCommentRepository, 
        rate_repository: AbstractRateRepository,
        place_repository: AbstractPlaceRepository,
        user_repository: AbstractUserRepository,
    ):
        self._comment_repository = comment_repository
        self._rate_repository = rate_repository
        self._place_repository = place_repository
        self._user_repository = user_repository

    async def run(self, request: RequestMessage) -> ResponseMessage:
        command = ModerationRequestCommand.from_mesage(request)
        
        users = await self._user_repository.list(
            tg_id=command.tg_id,
            is_admin=True
        )
        
        if len(users) == 0:
            return ResponseMessage(
                _tg_id=request._tg_id,
                _response_params={
                    'success': False
                },
                _text=f'У вас нет прав на выполнение данной команды',
            )
        
        if command.prev_comment_id is not None:
            if command.accept:
                await self._comment_repository.update(
                    comment_id=command.prev_comment_id,
                    is_moderated=True
                )
            else:
                await self._comment_repository.delete(
                    comment_id=command.prev_comment_id
                )
                command.place_offset -= 1
                if command.place_offset < 0:
                    command.place_offset == 0
        
        comments = await self._comment_repository.list(
            limit=1,
            offset=command.place_offset,
            is_moderated=False
        )
        
        if len(comments) == 0:
            return ResponseMessage(
                _tg_id=request._tg_id,
                _response_params={
                    'success': False
                },
                _text=f'Комментарии закончились.',
            )
        
        place = await self._place_repository.get(place_id=comments[0].place_id)
        rates = await self._rate_repository.list(place_id=comments[0].place_id, user_id=comments[0].user_id)
        
        response = ModerationResponse(
            comment_id=comments[0].comment_id,
            place=place.name,
            place_offset=command.place_offset + 1,
            rate=rates[0].rate,
            text=comments[0].text,
            tg_id=command.tg_id
        )
        
        return response.to_mesage()
    