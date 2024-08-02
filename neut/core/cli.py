import typer
import os
from slugify import slugify

from neut.utils.string import secure_token

app = typer.Typer()

def create_directory(path):
    os.makedirs(path, exist_ok=True)

@app.command()
def create_project(project_name: str):
    typer.echo(f"Creating new Neut project: {project_name}")
    
    create_directory(project_name)
    create_directory(os.path.join(project_name, "core"))
    create_directory(os.path.join(project_name, "apps"))
    
    with open(os.path.join(project_name, "main.py"), "w") as f:
        f.write("""from neut.core.app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
""")
    
    with open(os.path.join(project_name, "core/settings.py"), "w") as f:
        f.write(f"""from typing import List
from pathlib import Path

# Neut Project Settings
PROJECT_NAME = "{project_name.capitalize()}"

# Set this to False during production
DEBUG: bool = True

# Set this to a Secure Random string during production
SECRET_KEY: str = "neut_secret_key_{secure_token()}"

# This is your Project Root
BASE_DIR: Path = Path(__file__).parent.parent

# This whitelists hosts
ALLOWED_HOSTS: List[str] = ["*"]

FRONTEND_URL: str = "http://localhost:8000"

# This connects to your Database
DATABASE_URL: str = "sqlite:///./{slugify(project_name)}.db"

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
MAIL_USERNAME: str = ""
MAIL_PASSWORD: str = ""
MAIL_FROM: str = ""
MAIL_PORT: int = 587
MAIL_SERVER: str = ""
""")
    
    # Create Site app
    os.chdir(project_name)
    create_app("site")
    os.chdir("../")

    typer.echo(f"Project {project_name} created successfully!")

@app.command()
def create_app(app_name: str):
    typer.echo(f"Creating new Neut app: {app_name}")

    app_name = slugify(app_name, separator="_")
    app_prefix = "" if app_name == "site" else f"/{app_name}"
    
    app_dir = os.path.join("apps", app_name)
    create_directory(app_dir)
    
    open(os.path.join(app_dir, "__init__.py"), "w").close()
    
    with open(os.path.join(app_dir, "models.py"), "w") as f:
        f.write("""from sqlmodel import SQLModel, Field

# Define your models here
""")
        
    with open(os.path.join(app_dir, "routes.py"), "w") as f:
        f.write(f"""from neut.core.router import NeutRouter

router = NeutRouter(prefix="{app_prefix}")

@router.get("/")
async def root():
    return {{"message": "Welcome to the {app_name.capitalize()} app!"}}
""")
    
    typer.echo(f"App {app_name} created successfully!")

if __name__ == "__main__":
    app()