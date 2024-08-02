import asyncio
from social_core.strategy import BaseStrategy
from fastapi import Request
from neut.core.settings import settings

class NeutSocialStrategy(BaseStrategy):
    def __init__(self, app, storage=None):
        self.app = app
        self.storage = storage
        super().__init__(storage)

    def request_data(self, request: Request, *args, **kwargs):
        # TODO: Improve this to be fully asynchronous
        async def async_request_data():
            form_data = await request.form()
            return {
                **request.query_params,
                **form_data,
                **request.path_params
            }
        
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(async_request_data())

    def request_host(self, request: Request):
        return request.headers.get('host')

    def session_get(self, request: Request, name):
        return request.session.get(name)

    def session_set(self, request: Request, name, value):
        request.session[name] = value

    def session_pop(self, request: Request, name):
        return request.session.pop(name, None)

    def build_absolute_uri(self, request: Request, path=None):
        return str(request.url_for(path or request.url.path))

    def get_setting(self, name):
        return getattr(settings, name, None)