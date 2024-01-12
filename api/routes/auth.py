from typing import Annotated

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import app.models as m
from api.dependency import get_db
from api.oauth2 import create_access_token
from app import schema as s
from app.logger import log

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=s.Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)):
    """Logs in a user"""
    user = m.User.authenticate(form_data.username, form_data.password, session=db)
    if not user:
        log(log.ERROR, "User [%s] wrong username or password", form_data.username)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    log(log.INFO, "User [%s] logged in", user.username)
    return s.Token(access_token=create_access_token(user.id))


@router.post("/token", status_code=status.HTTP_200_OK, response_model=s.Token)
def get_token(auth_data: s.Auth, db=Depends(get_db)):
    """Logs in a user"""
    user = m.User.authenticate(auth_data.username, auth_data.password, session=db)
    if not user:
        log(log.ERROR, "User [%s] wrong username or password", auth_data.username)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    return s.Token(access_token=create_access_token(user.id))


@router.post("/google", status_code=status.HTTP_200_OK, response_model=s.Token)
def google_auth(
    data: s.GoogleAuthUser,
    db: Session = Depends(get_db),
):
    user: m.User | None = db.query(m.User).filter(sa.func.lower(m.User.email) == sa.func.lower(data.email)).first()

    password = "*"

    if not user:
        new_user: m.User = m.User(
            email=data.email,
            username=data.first_name,
            google_openid_key=data.uid,
            password=password,
        )
        db.add(new_user)

        try:
            db.commit()
        except SQLAlchemyError as e:
            log(log.INFO, "Error - [%s]", e)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Error while saving creating a user",
            )

        log(
            log.INFO,
            "User [%s] has been created (via Google account))",
            new_user.email,
        )
        user = new_user

    auth_user: m.User | None = m.User.authenticate(user.email, password, db)

    if not auth_user:
        log(log.ERROR, "User [%s] was not authenticated", data.email)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token: str = create_access_token(user.id)
    log(log.INFO, "Access token for User [%s] generated", auth_user.email)
    return s.Token(
        access_token=access_token,
        token_type="Bearer",
    )
