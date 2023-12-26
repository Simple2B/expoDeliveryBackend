from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(
        from_attributes=True,
    )


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

    model_config = ConfigDict(
        from_attributes=True,
    )
