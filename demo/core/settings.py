import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Neut Project Settings
PROJECT_NAME = "Demo"

# Set this to False during production
DEBUG: bool = True

# Set this to a Secure Random string during production
SECRET_KEY: str = "neut_secret_key_p(#A7pxrzscf@SFxhHh!6t6f_DM^Qqu^"

# This is your Project Root
BASE_DIR: Path = Path(__file__).parent.parent

# This whitelists hosts
ALLOWED_HOSTS: List[str] = ["*"]

FRONTEND_URL: str = "http://localhost:8000"

# This connects to your Database
DATABASE_URL: str = "sqlite:///./demo.db"

# This is a list of Neut Apps
INSTALLED_APPS: List[str] = [
    # Builtin Neut apps
    "neut.auth",
    # "neut.notifications",
    # "neut.events",
    # "neut.tasks",
    
    # Thirdparty and your apps
    "apps.site",
]

# This is a list of Neut middlewares
MIDDLEWARES: List[str] = [
    "neut.core.middleware.cors_middleware",
    "neut.core.middleware.authentication_middleware",
    # add your custom middleware
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

SOCIAL_AUTH_BACKENDS: List[str] = [
    'neut.auth.social.NeutGoogleOAuth2',
    'neut.auth.social.NeutFacebookOAuth2',
]

# OAuth2 settings
OAUTH2_STATE_TIMEOUT: int = 3600

# SMTP Mail Settings
MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
MAIL_FROM: str = os.getenv("MAIL_FROM")
MAIL_PORT: int = int(os.getenv("MAIL_PORT"))
MAIL_SERVER: str = os.getenv("MAIL_SERVER")
