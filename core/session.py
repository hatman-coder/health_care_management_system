from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database import database

engine = create_engine(database.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
