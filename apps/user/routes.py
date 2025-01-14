from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from .crud import create_user, get_user, update_user, delete_user
from .schema import UserCreate, UserUpdate, UserRead
from core.session import get_db
from uuid import UUID
from apps.user.models import User
from apps.authorization.routes import oauth2_scheme

router = APIRouter()


@router.post("/", response_model=UserRead)
async def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.get("/{user_id}", response_model=UserRead)
async def get_user_route(
    user_id: UUID, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    user_obj = get_user(db=db, user_id=user_id)
    if user_obj is None:
        return JSONResponse("User not found", 404)
    return user_obj


@router.get("/", response_model=List[UserRead])
async def get_users_route(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    users = db.query(User).all()
    return users


@router.put("/{user_id}", response_model=UserRead)
async def update_user_route(
    user_id: UUID,
    user: UserUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user_obj = get_user(db=db, user_id=user_id)
    if user_obj is None:
        return JSONResponse("Invalid User ID", 400)
    return update_user(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}", response_model=UserRead)
async def delete_user_route(
    user_id: UUID, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    user_obj = get_user(db=db, user_id=user_id)
    if user_obj is None:
        return JSONResponse("Invalid User ID", 400)
    return delete_user(db=db, user_id=user_id)
