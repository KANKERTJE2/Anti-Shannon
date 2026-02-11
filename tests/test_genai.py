import pytest
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
        Middleware(WukongMiddleware, enable_genai_traps=True)
    ]
    return TestClient(Starlette(routes=routes, middleware=middleware))

def test_genai_user_trap(client):
    """Test that users route returns fake user data"""
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) >= 5
    assert "email" in data["data"][0] 
    # Faker generates random emails, so we just check key existence
