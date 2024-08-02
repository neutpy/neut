from neut.core.router import NeutRouter

def test_neut_router():
    router = NeutRouter()
    
    @router.get("/test")
    def test_route():
        return {"message": "test"}
    
    assert len(router.routes) == 1
    assert router.routes[0].path == "/test"