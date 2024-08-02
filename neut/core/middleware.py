from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from neut.core.settings import settings

def cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def authentication_middleware(app: FastAPI):
    # Implement your authentication middleware here
    pass

def setup_middleware(app: FastAPI):
    cors_middleware(app)
    authentication_middleware(app)