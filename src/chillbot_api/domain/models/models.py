from pydantic import BaseModel


class Place(BaseModel):
    place_id: int
    city: str
    category: str
    name: str
    

class Comment(BaseModel):
    comment_id: int
    text: str
    is_moderated: bool
    user: str
    place: str
    place_id: int
    rate_id: int
    rate: int
    