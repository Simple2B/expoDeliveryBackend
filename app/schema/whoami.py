from pydantic import BaseModel


class WhoAmIOut(BaseModel):
    unique_id: str
    is_auth_by_google: bool
    is_auth_by_apple: bool
