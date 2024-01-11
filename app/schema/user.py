from pydantic import BaseModel, ConfigDict, EmailStr, AnyHttpUrl


class User(BaseModel):
    id: int
    username: str
    email: str
    activated: bool = True

    model_config = ConfigDict(
        from_attributes=True,
    )


class GoogleAuthUser(BaseModel):
    email: str | EmailStr
    first_name: str = ""
    photo_url: AnyHttpUrl | str | None
    uid: str | None
