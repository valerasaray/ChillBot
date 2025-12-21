import random
from domain.command.moderation import ModerationRequestCommand, ModerationResponse
from domain.models.models import Comment, Place
from domain.llm.message import LlmMessage
from domain.message.request_message import RequestMessage
from domain.message.response_message import ResponseMessage
from domain.command.recomend import RecomendCommand
from services.repositories.abstract_user_repository import AbstractUserRepository
from services.repositories.abstract_comment_repository import AbstractCommentRepository
from services.repositories.abstract_place_repository import AbstractPlaceRepository
from services.repositories.abstract_rate_repository import AbstractRateRepository
from services.llm.abstract_llm_client import AbstractLlmClient
from services.logger.logger import logger
from usecases.command.abstract_command import AbstractCommand
from domain.llm.message import RecomendLlmMessage, CommentsLlmMessage
from domain.command.recomend import RecomendComment


class Recomend(AbstractCommand):
    def __init__(
        self,
        llm_client: AbstractLlmClient,
        comment_repository: AbstractCommentRepository, 
        rate_repository: AbstractRateRepository,
        place_repository: AbstractPlaceRepository,
        user_repository: AbstractUserRepository,
    ):
        self._comment_repository = comment_repository
        self._rate_repository = rate_repository
        self._place_repository = place_repository
        self._user_repository = user_repository
        self._llm_client = llm_client
    
    async def run(self, request: RequestMessage) -> ResponseMessage:
        command = RecomendCommand.from_message(request)
        
        if command.category is None or command.city is None:
            rec_llm_request = RecomendLlmMessage(
                text=command.message,
                context=command.context,
                comments=command.comments,
                success=command.success,
                category=command.category,
                city=command.city,
                clarification_category=None,
                clarification_city=None,
            )
            
            rec_llm_response = RecomendLlmMessage(
                text='',
                context=command.context,
                success=False
            )
            
            for _ in range(10):
                try:
                    rec_llm_response = self._llm_client.invoke(
                        prompt=rec_llm_request.to_prompt(),
                        message=RecomendLlmMessage,        
                    )
                    break
                except Exception as e:
                    logger.error(e.with_traceback())
                    continue
                
            logger.info(rec_llm_response)
                
        if (
            rec_llm_response.clarification_category is None and 
            rec_llm_response.clarification_city is None and 
            rec_llm_response.category is not None and 
            rec_llm_response.city is not None
        ):
            places = await self._place_repository.list(
                category=rec_llm_response.category,
                city=rec_llm_response.city 
            )
            
            if len(places) == 0:
                return ResponseMessage(
                    _tg_id=command.tg_id,
                    _command='recomend',
                    _context=command.context,
                    _text='Не удалось найти место по Вашему запросу, попробуйте поискать что-нибудь еще.',
                    _response_params={
                        'success': False,
                        'fatal': True,
                        'city': None,
                        'category': None,
                        'comments': None,
                    }
                )
            
            top_places: list[tuple[int, Place, list[str]]] = []
            
            for place in places:
                place = Place(
                    category=place.category,
                    city=place.city,
                    name=place.name,
                    place_id=place.place_id
                )
                
                comment_dtos: list[RecomendComment] = []
                
                comments = await self._comment_repository.list(
                    is_moderated=True,
                    place_id=place.place_id
                )
                
                common_rating_val = 0
                for comment in comments:
                    rate = await self._rate_repository.list(
                        user_id=comment.user_id,
                        place_id=place.place_id
                    )
                    common_rating_val += rate[0].rate
                    comment_dtos.append(RecomendComment(
                        rate=rate[0].rate,
                        text=comment.text
                    ))
                    
                comment_texts = [c.text for c in comment_dtos]
                
                if len(comment_dtos) > 0:
                    rating_req = common_rating_val / len(comment_dtos)
                else:
                    rating_req = 0
                comments_req: list[str] = []
                if len(comment_dtos) > 0: 
                    for _ in range(5):
                        k = random.randint(0, len(comment_dtos) - 1)
                        comments_req.append(comment_texts[k])

                top_places.append(
                    (
                        rating_req,
                        place,
                        comments_req
                    )
                )
                
            top_places = sorted(top_places, key=lambda p: p[0])
            
            logger.info(top_places)
            
            text = '\n'
            
            for i in range(min(len(top_places), 3)):
                comment_llm_req = CommentsLlmMessage(
                    category=top_places[i][1].category,
                    city=top_places[i][1].city,
                    place=top_places[i][1].name,
                    comments=top_places[i][2],
                    rating=top_places[i][0],
                    summary=None
                )
                
                comment_llm_res = CommentsLlmMessage(summary='')
                
                for _ in range(10):
                    try:
                        comment_llm_res = self._llm_client.invoke(
                            prompt=comment_llm_req.to_prompt(),
                            message=CommentsLlmMessage
                        )
                        break
                    except Exception as ex:
                        logger.error(ex.with_traceback())
                        continue
                
                text += f'{comment_llm_res.summary}\n'
            
            return ResponseMessage(
                _tg_id=command.tg_id,
                _command='recomend',
                _context=command.context,
                _text=text,
                _response_params={
                    'success': True,
                    'fatal': False,
                    'city': place.city,
                    'category': place.category,
                    'comments': comment_dtos,
                }
            )
            
        else:
            text = '\n'
            
            if rec_llm_response.clarification_city is not None:
                text += f'{rec_llm_response.clarification_city}\n'
            
            if rec_llm_response.clarification_category is not None:
                text += f'{rec_llm_response.clarification_category}'
            
            return ResponseMessage(
                _tg_id=command.tg_id,
                _context=command.context,
                _text=text,
                _command='recomend',
                _response_params={
                    'success': False,
                    'fatal': False,
                    'city': rec_llm_response.city,
                    'category': rec_llm_response.category,
                    'comments': None,
                }
            )
            
