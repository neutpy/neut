from neut.core.router import NeutRouter

router = NeutRouter(prefix="")

@router.get("/")
async def root():
    return {"message": "Welcome to the Site app!"}
