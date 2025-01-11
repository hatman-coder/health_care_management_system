from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from .crud import create_user, get_user, update_user, delete_user
from .schema import UserCreate, UserUpdate, UserRead
from core.session import get_db
from uuid import UUID
from apps.user.models import User

router = APIRouter()


@router.post("/", response_model=UserRead)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.get("/{user_id}", response_model=UserRead)
def get_user_route(user_id: UUID, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        return JSONResponse("User not found", 404)
    return db_user


@router.get("/", response_model=List[UserRead])
def get_users_route(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.put("/{user_id}", response_model=UserRead)
def update_user_route(user_id: UUID, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        return JSONResponse("User not found", 404)
    return db_user


@router.delete("/{user_id}", response_model=UserRead)
def delete_user_route(user_id: UUID, db: Session = Depends(get_db)):
    db_user = delete_user(db=db, user_id=user_id)
    if db_user is None:
        return JSONResponse("User not found", 404)
    return db_user
