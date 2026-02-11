import pytest
from starlette.testclient import TestClient
from wukong.middleware import WukongMiddleware
from wukong.traps.tokens import HoneyTokenGenerator
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.routing import Route

@pytest.fixture
def client():
    # We need to reset the middleware state because Vacuum/HoneyToken use memory storage
    # for the prototype.
    
    async def homepage(request): return JSONResponse({"message": "Welcome"})

    routes = [Route("/", homepage)]
    middleware = [
        Middleware(WukongMiddleware, enable_vacuum=True, enable_honey_traps=True, enable_probe_detection=True, enable_route_shifting=True, enable_honey_tokens=True)
    ]
    return TestClient(Starlette(routes=routes, middleware=middleware))

def test_honeytoken_block_middleware(client):
    """Test that middleware successfully blocks a generated honeytoken"""
    # 1. Generate a token (shared state allows middleware to see it)
    gen = HoneyTokenGenerator()
    token = gen.generate_token()
    
    # 2. Use it in a request
    response = client.get("/", headers={"Authorization": f"Bearer {token}"})
    
    # 3. Should be blocked (401)
    assert response.status_code == 401
    assert response.json() == {"error": "Unauthorized"}

def test_normal_token_pass(client):
    """Test that random tokens are NOT blocked (unless app blocks them, but middleware shouldn't specificially trap them)"""
    response = client.get("/", headers={"Authorization": "Bearer random-token-123"})
    # The example app returns 200 for /, ignoring auth. 
    # Middleware shouldn't block it because it's not a honeytoken.
    assert response.status_code == 200
