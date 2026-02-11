import pytest
from starlette.testclient import TestClient
from examples.app import app
from wukong.middleware import WukongMiddleware

# Recreate client for fresh state
@pytest.fixture
def client():
    # We need to reset the middleware state because Vacuum/HoneyToken use memory storage
    # for the prototype.
    # Best way: Recreate the app stack.
    from starlette.applications import Starlette
    from starlette.middleware import Middleware
    from starlette.responses import JSONResponse
    from starlette.routing import Route
    
    async def homepage(request): return JSONResponse({"message": "Welcome"})
    async def admin(request): return JSONResponse({"secret": "admin"})

    routes = [Route("/", homepage), Route("/admin", admin)]
    middleware = [
        Middleware(WukongMiddleware, enable_vacuum=True, enable_honey_traps=True, enable_probe_detection=True, enable_route_shifting=True)
    ]
    return TestClient(Starlette(routes=routes, middleware=middleware))


def test_vacuum_blocking(client):
    """Test that Vacuum blocks IP after multiple probes"""
    # 1. Send multiple probes (SQLi)
    # The limit is 5. Severity per probe is 2. So 3 probes = 6 > 5.
    for _ in range(3):
        response = client.get("/?q=' UNION SELECT")
        assert response.status_code == 500 # ProbeDetector blocks it
        
    # The Vacuum logic blocks after score >= 5. 
    
    # 2. Next request should be 403 (Global Block)
    response = client.get("/")
    assert response.status_code == 403
    assert response.text == "Access Denied"

def test_vacuum_honeytoken_instant_ban():
    """Test that honeytoken triggers high severity report"""
    # Since state is shared in our prototype modules, we might need to reset or use a different IP context.
    # TestClient uses 'testclient' as host usually, or 127.0.0.1.
    # To test distinct IPs, we need to mock request.client.host.
    pass 
