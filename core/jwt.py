import secrets

# Configuration
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_EXPIRE_MINUTES = 30
