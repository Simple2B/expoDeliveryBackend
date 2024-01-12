from pydantic import BaseModel, ConfigDict
from .restaurant import Restaurant
from .category import Category


class BaseFood(BaseModel):
    id: int
    uuid: str
    name: str
    image: str
    info: str

    price: float
    calories: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class Food(BaseFood):
    restaurants: list[Restaurant]
    tags: list[Category]


class FoodList(BaseModel):
    foods: list[Food]
