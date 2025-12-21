import json

from pydantic import BaseModel
from domain.prompt.recomendation_prompt import create_recommendation_prompt
from domain.prompt.comments_prompt import create_comments_prompt
from domain.command.recomend import RecomendComment
from services.logger.logger import logger


class LlmMessage(BaseModel):
    def to_prompt(self) -> str:
        return ''

    @staticmethod
    def from_json(data: str) -> 'LlmMessage':
        pass


class RecomendLlmMessage(LlmMessage):
    text: str
    context: str
    success: bool
    city: str | None = None
    category: str | None = None
    comments: dict[str, list[RecomendComment]] | None = None
    clarification_city: str | None = None
    clarification_category: str | None = None
    
    @staticmethod
    def from_json(data: str) -> 'RecomendLlmMessage':
        json_data = json.loads(data)
        logger.info(json_data)
        
        text = ''
        if json_data['clarification_city'] is not None:
            text += json_data['clarification_city']
        if json_data['clarification_category'] is not None:
            text += json_data['clarification_category']
        
        return RecomendLlmMessage(
            text=text,
            context=text,
            category=json_data['category'],
            city=json_data['city'],
            success=json_data['success'],
            clarification_category=json_data['clarification_category'],
            clarification_city=json_data['clarification_city']
        )
        
    
    def to_prompt(self) -> str:
        return create_recommendation_prompt(
            user_text=self.text, 
            user_context=self.context,
            cities=[
                'Москва',
                'Санкт-Петербург',
                'Минск',
                'Новосибирск',
                'Екатеринбург',
                'Казань',
                'Нижний Новгород',
                'Челябинск, Россия',
                'Самара',
                'Омск',
                'Ростов-на-Дону',
                'Уфа',
                'Красноярск',
                'Воронеж',
                'Пермь',
                'Волгоград',
                'Краснодар',
                'Саратов',
                'Тольятти',
                'Ижевск',
                'Барнаул',
                'Ульяновск',
                'Тюмень',
                'Иркутск',
                'Хабаровск',
                'Ярославль',
                'Владивосток',
                'Махачкала',
                'Томск',
                'Оренбург',
                'Кемерово',
                'Новокузнецк',
                'Рязань',
                'Астрахань',
                'Пенза',
                'Липецк',
                'Тула',
                'Киров',
                'Чебоксары',
                'Калининград',
                'Брянск',
                'Магнитогорск',
                'Иваново',
                'Тверь',
                'Ставрополь',
                'Белгород',
                'Сочи',
                'Владимир',
                'Архангельск',
                'Калуга',
                'Сургут'
            ],
            categories = [
                'theatre', 'cafe', 'museum', 'restaurant', 'bar', 'pub',
                'attraction', 'nightclub', 'cinema', 'fast_food', 'mall', 'arts_centre',
                'stripclub', 'food_court', 'gallery', 'bbq', 'love_hotel', 'zoo',
                'fountain', 'aquarium', 'camp_pitch', 'brothel', 'swingerclub', 'exhibition_centre',
                'events_centre', 'planetarium', 'community_centre', 'books', 'library', 'casino',
                'gambling'
            ]
        )
    

class CommentsLlmMessage(LlmMessage):
    place: str | None = None
    city: str | None = None
    category: str | None = None
    rating: int | None = None
    comments: list[str] | None = None
    summary: str | None = None
    
    def to_prompt(self) -> str:
        return create_comments_prompt(self.place, self.city, self.category, self.rating, self.comments)

    @staticmethod
    def from_json(data: str) -> 'CommentsLlmMessage':
        data_json = json.loads(data)
        return CommentsLlmMessage(
            summary=data_json['summary']
        )