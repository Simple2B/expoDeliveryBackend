from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str
    image: str


class Filters(BaseModel):
    id: int
    name: str
    count: int
