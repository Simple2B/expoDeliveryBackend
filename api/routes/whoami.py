from fastapi import APIRouter, status, Depends

import app.models as m
import app.schema as s
from api.dependency import get_current_user
from app.logger import log
from config import config, DevelopmentConfig, TestingConfig, ProductionConfig


whoami_router = APIRouter(prefix="/whoami", tags=["Whoami"])

settings: DevelopmentConfig | TestingConfig | ProductionConfig = config()


@whoami_router.get("/user", status_code=status.HTTP_200_OK, response_model=s.WhoAmIOut)
def whoami(
    current_user: m.User = Depends(get_current_user),
    app_version: str | None = None,
):
    if app_version:
        log(log.INFO, "App version for user [%s]: [%s]", current_user.email, app_version)

    return s.WhoAmIOut(
        unique_id=current_user.unique_id,
        is_auth_by_google=current_user.is_auth_by_google,
        is_auth_by_apple=current_user.is_auth_by_apple,
    )
