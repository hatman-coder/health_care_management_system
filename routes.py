from fastapi import FastAPI
from apps.user.urls import router as user_router

app = FastAPI()

# USER APP
app.include_router(user_router, prefix="/users", tags=["users"])
