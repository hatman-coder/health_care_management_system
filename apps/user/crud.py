from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from .models import User
from .schema import UserCreate, UserUpdate
from fastapi.responses import JSONResponse
from external.pass_hasher import hash_password


def create_user(db: Session, user: UserCreate):
    new_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        return JSONResponse("Email is already registered! Try another one", 406)
    return JSONResponse("User created", 201)


def get_user(db: Session, user_id: UUID):
    return db.query(User).filter(User.user_id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: UUID, user: UserUpdate):
    user_obj = db.query(User).filter(User.user_id == user_id).first()
    if user_obj:
        if user.name:
            user_obj.name = user.name
        if user.email:
            user_obj.email = user.email
        if user.role:
            user_obj.role = user.role
        db.commit()
        db.refresh(user_obj)
    return JSONResponse("User updated", 200)


def delete_user(db: Session, user_id: UUID):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return JSONResponse("User deleted", 200)
