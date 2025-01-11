from fastapi import FastAPI
from core.session import engine
from base.base import Base
from routes import app as FastAPIObject
from contextlib import contextmanager
from sqladmin import Admin, ModelView
from apps.user.models import User


@contextmanager
def db_connect():
    try:
        engine.connect()
        # Create all tables
        Base.metadata.create_all(engine)
        yield
    except Exception as e:
        print(f"Error during application setup: \n{e}\n")
    finally:
        engine.dispose()


def start_application():
    with db_connect():
        pass
    return FastAPIObject


app = start_application()
