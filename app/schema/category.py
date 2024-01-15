from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    id: int
    name: str
    image: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class Filter(BaseModel):
    id: int
    name: str
    count: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class ChosenFilters(BaseModel):
    categories: list[int]
    min_price: float | None
    max_price: float | None
    min_calories: int | None
    max_calories: int | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class CategoryList(BaseModel):
    categories: list[Category]

    model_config = ConfigDict(
        from_attributes=True,
    )


class FilterList(BaseModel):
    filters: list[Filter]

    model_config = ConfigDict(
        from_attributes=True,
    )
