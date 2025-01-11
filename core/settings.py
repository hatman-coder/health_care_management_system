from decouple import config
from urllib.parse import quote

class Database:
    DB_NAME: str = config("DB_NAME")
    DB_USER: str = config("DB_USER")
    DB_PASSWORD: str = quote(config("DB_PASSWORD"))
    DB_SERVER: str = config("DB_SERVER")
    DB_PORT: str = config("DB_PORT")

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"



database = Database()