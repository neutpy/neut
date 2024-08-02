from fastapi import APIRouter

class NeutRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any custom functionality here