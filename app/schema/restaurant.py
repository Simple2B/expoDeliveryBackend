from pydantic import BaseModel

from .category import Category


class PanelRestaurant(BaseModel):
    id: int
    name: str
    image: str
    duration: str
    distance: float
    rate: str
    rates: int
    tags: list[Category]


class Restaurant(BaseModel):
    id: int
    name: str
    image: str
    duration: str
    distance: float
    rate: str
    rates: int
    tags: list[Category]
    description: str
    is_deleted: bool
    created_at: str
    location: str
