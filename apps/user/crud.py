from sqlalchemy.orm import Session
from uuid import UUID
from .models import User
from .schema import UserCreate, UserUpdate
from fastapi.responses import JSONResponse


def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name, email=user.email, password=user.password, role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return JSONResponse("User created", 201)


def get_user(db: Session, user_id: UUID):
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: UUID, user: UserUpdate):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        if user.name:
            db_user.name = user.name
        if user.email:
            db_user.email = user.email
        if user.password:
            db_user.password = user.password
        if user.role:
            db_user.role = user.role
        db.commit()
        db.refresh(db_user)
    return JSONResponse("User updated", 200)


def delete_user(db: Session, user_id: UUID):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
