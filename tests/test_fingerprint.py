import pytest
import hashlib
from starlette.testclient import TestClient
from wukong.middleware import WukongMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.routing import Route

@pytest.fixture
def client():
    async def homepage(request): return JSONResponse({"message": "Welcome"})
    routes = [Route("/", homepage)]
    middleware = [
        Middleware(WukongMiddleware, enable_fingerprinting=True, enable_vacuum=True)
    ]
    return TestClient(Starlette(routes=routes, middleware=middleware))

def test_fingerprint_bot_headers(client):
    """Test that a bot-like user agent triggers warning (doesn't block by default in prototype unless threshold hit)"""
    # Vacuum blocks after score >= 5. Bot detection severity is 1.
    # So we need 5 hits to block.
    
    headers = {"User-Agent": "python-requests/2.28.1"}
    for _ in range(5):
        client.get("/", headers=headers)
        
    # 6th request should be blocked by Vacuum
    response = client.get("/", headers=headers)
    assert response.status_code == 403
