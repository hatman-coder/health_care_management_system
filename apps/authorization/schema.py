from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# Pydantic schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserInDB(BaseModel):
    user_id: UUID
    username: str
    email: str
    role: str
    password: str
