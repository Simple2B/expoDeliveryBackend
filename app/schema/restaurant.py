from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .category import Category


class PanelRestaurant(BaseModel):
    id: int
    name: str
    image: str
    duration: str
    distance: float
    rate: float
    rates: int
    tags: list[Category]

    model_config = ConfigDict(
        from_attributes=True,
    )


class Restaurant(BaseModel):
    id: int
    name: str
    image: str
    duration: str
    distance: float
    rate: float
    rates: int
    tags: list[Category]
    description: str
    is_deleted: bool
    created_at: datetime
    location: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class PanelRestaurantList(BaseModel):
    panels: list[PanelRestaurant]

    model_config = ConfigDict(
        from_attributes=True,
    )


class RestaurantList(BaseModel):
    restaurants: list[Restaurant]

    model_config = ConfigDict(
        from_attributes=True,
    )
