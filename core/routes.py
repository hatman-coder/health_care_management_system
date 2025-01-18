from fastapi import FastAPI
from apps.user.routes import router as user_router
from apps.authorization.routes import router as login_router
from base.homepage import router as homepage_router
from fastapi.middleware.cors import CORSMiddleware
from core.middleware import TokenValidationMiddleware
from fastapi.staticfiles import StaticFiles

swagger_ui_default_parameters = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "docExpansion": "none",
    "showExtensions": True,
    "showCommonExtensions": True,
    # "defaultModelsExpandDepth": -1,
}


app = FastAPI(swagger_ui_parameters=swagger_ui_default_parameters)

# CORS ALLOWED ORIGINS
origins = [
    "http://localhost",
]


# MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TokenValidationMiddleware)

# Routes
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(login_router, prefix="/auth", tags=["Auth"])
app.include_router(homepage_router, prefix="", tags=["Homepage"])

# STATIC DIR
app.mount("/static", StaticFiles(directory="static"), name="static")
