from fastapi import FastAPI
from neut.core.middleware import setup_middleware

def test_middleware_setup():
    app = FastAPI()
    setup_middleware(app)
    middleware_types = [type(m) for m in app.user_middleware]
    assert any('Middleware' in str(m) for m in middleware_types)