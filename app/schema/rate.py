from pydantic import BaseModel, ConfigDict


class Rate(BaseModel):
    id: int
    name: str
    image: str
    duration: str
    distance: float
    rate: str
    rates: int

    model_config = ConfigDict(
        from_attributes=True,
    )
