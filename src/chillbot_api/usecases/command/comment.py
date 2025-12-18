from domain.models.models import Comment, Place
from domain.message.request_message import RequestMessage
from domain.message.response_message import ResponseMessage
from domain.command.comment import CommentCommand
from services.repositories.abstract_user_repository import AbstractUserRepository
from services.repositories.abstract_comment_repository import AbstractCommentRepository
from services.repositories.abstract_place_repository import AbstractPlaceRepository
from services.repositories.abstract_rate_repository import AbstractRateRepository
from usecases.command.abstract_command import AbstractCommand


class Comment(AbstractCommand):
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
        command = CommentCommand.from_mesage(request)
        
        place_records = await self._place_repository.list(name=command.place_name)
        if len(place_records) == 0:
            return ResponseMessage(
                _tg_id=request._tg_id,
                _response_params={
                    'success': False
                },
                _text=f'Места {command.place_name} нет в базе, поищите что-нибудь еще',
            )
        
        place = Place(
            category=place_records[0].category,
            city=place_records[0].city,
            name=place_records[0].name,
            place_id=place_records[0].place_id
        )
        
        user_records = await self._user_repository.list(tg_id=request._tg_id)
        
        user_id = user_records[0].user_id
        
        old_comments = await self._comment_repository.list(
            place_id=place.place_id,
            user_id=user_id
        )
        old_rates = await self._comment_repository.list(
            place_id=place.place_id,
            user_id=user_id
        )

        if len(old_rates) == 0 and len(old_comments) == 0:
            await self._comment_repository.create(
                is_moderated=False,
                place_id=place.place_id,
                text=command.text,
                user_id=user_id
            )
            await self._rate_repository.create(
                user_id=user_id,
                place_id=place.place_id,
                rate=command.rate
            )
            
            return ResponseMessage(
                _tg_id=request._tg_id,
                _response_params={
                    'success': True
                },
                _text=f'Создан новый отзыв на место отдыха {command.place_name}',
            )
        
        comment_id = old_comments[0].comment_id
        rate_id = old_rates[0].rate_id
        await self._comment_repository.update(
            comment_id=comment_id,
            is_moderated=False,
            text=command.text
        )
        await self._rate_repository.update(
            rate_id=rate_id,
            rate=command.rate
        )
        
        return ResponseMessage(
            _tg_id=request._tg_id,
            _response_params={
                'success': True
            },
            _text=f'Обновлен отзыв на место отдыха {command.place_name}',
        )
