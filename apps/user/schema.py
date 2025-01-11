from pydantic import BaseModel, EmailStr
from uuid import UUID
from external.enum import UserRole
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    user_id: UUID
    name: str
    email: EmailStr
    role: UserRole
    # doctor: Optional["DoctorRead"] = None
    # patient: Optional["PatientRead"] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

    class Config:
        from_attributes = True
