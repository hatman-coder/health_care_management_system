from fastapi import Depends, APIRouter
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.session import get_db

from .schema import *
from .crud import create_access_token, create_access_token_using_refresh_token, logout

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/token", response_model=Token)
async def create_access_token_for_login_route(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    return create_access_token(db, form_data)


@router.post("/refresh", response_model=Token)
async def create_access_token_using_refresh_token_route(refresh_token: str):
    return create_access_token_using_refresh_token(refresh_token)


@router.post("/logout")
async def logout_route(token: str = Depends(oauth2_scheme)):
    return logout(token)
