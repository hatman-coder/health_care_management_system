import jwt
import secrets
import hashlib
import base64

from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from apps.user.models import User
from .schema import *
from external.pass_hasher import verify_password
from core.redis import add_to_blacklist, is_token_blacklisted
from core.jwt import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


def get_user(db: Session, username: str) -> Optional[UserInDB]:
    user = db.query(User).filter(User.username == username).first()
    if user:
        return UserInDB(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role,
            password=user.password,
        )
    return None


def authenticate_user(db: Session, email: str, password: str) -> Optional[UserInDB]:
    user = get_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def generate_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()

    # Generate a unique token ID (jti) with random hex + timestamp + hash
    unique_value = secrets.token_hex(16) + str(datetime.now(timezone.utc).timestamp())
    jti_hash = hashlib.sha256(unique_value.encode()).hexdigest()
    to_encode["jti"] = jti_hash

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})

    salt = secrets.token_urlsafe(16)
    to_encode["salt"] = salt

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    encoded_jwt = base64.urlsafe_b64encode(encoded_jwt.encode()).decode()

    return encoded_jwt


def generate_refresh_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()

    # Generate a unique token ID (jti) with random hex + timestamp + hash
    unique_value = secrets.token_hex(16) + str(datetime.now(timezone.utc).timestamp())
    jti_hash = hashlib.sha256(unique_value.encode()).hexdigest()
    to_encode["jti"] = jti_hash

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})

    salt = secrets.token_urlsafe(16)
    to_encode["salt"] = salt

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    encoded_jwt = base64.urlsafe_b64encode(encoded_jwt.encode()).decode()

    return encoded_jwt


def create_access_token(db, form_data):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return JSONResponse("Incorrect email or password", 401)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = generate_refresh_token(
        data={"sub": user.email},
        expires_delta=refresh_token_expires,
    )
    return Token(access_token=access_token, refresh_token=refresh_token)


def create_access_token_using_refresh_token(refresh_token: str):
    try:
        decoded_refresh_token = base64.urlsafe_b64decode(refresh_token).decode()
        payload = jwt.decode(decoded_refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        user_email = payload.get("sub")
        if not user_email:
            raise jwt.InvalidTokenError()

        jti = payload.get("jti")
        if jti:
            if is_token_blacklisted(jti):
                return JSONResponse("Refresh token is unauthorized or blocked")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = generate_access_token(
            data={"sub": user_email},
            expires_delta=access_token_expires,
        )

        return Token(access_token=new_access_token, refresh_token=refresh_token)

    except jwt.ExpiredSignatureError:
        return JSONResponse("Refresh token expired", 401)
    except jwt.InvalidTokenError:
        return JSONResponse("Invalid refresh token", 401)
    except Exception as e:
        return JSONResponse(e, 400)


def logout(token: str):
    try:
        decoded_token = base64.urlsafe_b64decode(token).decode()

        payload = jwt.decode(decoded_token, SECRET_KEY, algorithms=[ALGORITHM])

        jti = payload.get("jti")

        if not jti:
            return JSONResponse(content={"detail": "Invalid token"}, status_code=400)

        exp = payload.get("exp")
        if exp:
            expires_in = exp - int(datetime.now(timezone.utc).timestamp())

            add_to_blacklist(jti, expires_in)
            return JSONResponse(
                content={"detail": "Logged out successfully"}, status_code=200
            )
        else:
            return JSONResponse(
                content={"detail": "Invalid token: no expiration time found"},
                status_code=400,
            )

    except jwt.ExpiredSignatureError:
        return JSONResponse(content={"detail": "Token has expired"}, status_code=401)
    except jwt.InvalidTokenError:
        return JSONResponse(content={"detail": "Invalid token"}, status_code=401)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=400)
