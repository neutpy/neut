import importlib
from fastapi import FastAPI
from neut.core.settings import settings
from neut.core.middleware import setup_middleware
from neut.auth.strategy import NeutSocialStrategy
from social_core.backends.utils import load_backends

class NeutApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_middleware()
        self.load_apps()
        self.setup_social_auth()

    def setup_middleware(self):
        setup_middleware(self)

    def load_apps(self):
        for app in settings.INSTALLED_APPS:
            try:
                module = importlib.import_module(f"{app}.routes")
                self.include_router(module.router)
            except ImportError as e:
                print(e)
                print(f"Could not load app: {app}")

    def setup_social_auth(self):
        self.state.strategy = NeutSocialStrategy(self)
        self.state.social_auth_backends = load_backends(settings.SOCIAL_AUTH_AUTHENTICATION_BACKENDS)


app = NeutApp(title=settings.PROJECT_NAME)