from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Dict, Any
import importlib

class NeutSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    PROJECT_NAME: str = "Neut Project"
    
    DEBUG: bool = False
    
    SECRET_KEY: str = "your-secret-key"

    ALLOWED_HOSTS: List[str] = ["*"]

    FRONTEND_URL: str = "http://localhost:8000"

    BASE_DIR: Path = Path(__file__).parent.parent

    DATABASE_URL: str = "sqlite:///./neut.db"

    INSTALLED_APPS: List[str] = [
        "neut.auth",
        # "neut.notifications",
        # "neut.events",
        # "neut.tasks",
    ]

    MIDDLEWARES: List[str] = [
        "neut.core.middleware.cors_middleware",
        "neut.core.middleware.authentication_middleware",
    ]

    # Authentication & Authorizaton
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Social Auth settings
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: str = ""
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: str = ""
    SOCIAL_AUTH_FACEBOOK_KEY: str = ""
    SOCIAL_AUTH_FACEBOOK_SECRET: str = ""
    
    # Redirect URLs
    SOCIAL_AUTH_LOGIN_REDIRECT_URL: str = "/auth/social/success"
    SOCIAL_AUTH_LOGIN_ERROR_URL: str = "/auth/social/error"

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS: List[str] = [
        'neut.auth.social.NeutGoogleOAuth2',
        'neut.auth.social.NeutFacebookOAuth2',
    ]

    # OAuth2 settings
    OAUTH2_STATE_TIMEOUT: int = 3600

    # SMTP Mail Settings
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = ""

def load_project_settings() -> Dict[str, Any]:
    try:
        project_settings_module = importlib.import_module('core.settings')
        project_settings = {key: value for key, value in project_settings_module.__dict__.items() if not key.startswith('__')}
        return project_settings
    except ModuleNotFoundError:
        return {}

def merge_settings(default_settings: BaseSettings, project_settings: Dict[str, Any]) -> BaseSettings:
    for key, value in project_settings.items():
        if hasattr(default_settings, key):
            setattr(default_settings, key, value)
    return default_settings

# Load and merge settings
project_settings = load_project_settings()
settings = merge_settings(NeutSettings(), project_settings)
