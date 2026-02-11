import pytest
import asyncio
import time
from starlette.testclient import TestClient
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from wukong.middleware import WukongMiddleware

@pytest.fixture
def client_elite():
    async def homepage(request): 
        return HTMLResponse('<html><body><form action="/submit" method="post"><input type="text" name="user"><input type="submit"></form></body></html>')
    
    async def submit(request):
        return JSONResponse({"status": "success"})

    routes = [Route("/", homepage), Route("/submit", submit, methods=["POST"])]
    middleware = [
        Middleware(WukongMiddleware, enable_honey_fields=True, enable_tarpit=True, enable_vacuum=True)
    ]
    # Ensure client IP is set for TestClient
    return TestClient(Starlette(routes=routes, middleware=middleware))


def test_honey_field_injection(client_elite):
    """Test that hidden honey fields are injected into forms."""
    response = client_elite.get("/")
    assert response.status_code == 200
    # The field is chosen randomly, so check if any of the possible traps are present
    possible_traps = ["_admin_confirm", "secret_token", "verification_bypass", "internal_debug_id"]
    assert any(f'name="{field}"' in response.text for field in possible_traps)
    assert 'style="display:none' in response.text


def test_honey_field_trigger(client_elite):
    """Test that filling a honey field triggers a block."""
    # First request to get the session/IP context (TestClient handles this)
    # Trigger the trap
    response = client_elite.post("/submit", data={"user": "mikaeel", "_admin_confirm": "bot_value"})
    assert response.status_code == 400
    assert "Hidden field detected" in response.json().get("message", "")

def test_tar_pit_delay(client_elite):
    """Test that repeated suspicious requests result in increasing delays."""
    # Trigger suspicion first (using the honey field again)
    # We'll use the middleware directly to increase suspicion or just trigger it
    
    # 1. First trigger (Score becomes 2 because honeyfield triggers severity 5 report which adds to score)
    # Wait, honeyfield triggers severity 5 report. Vacuum score >= 5 blocks. 
    # Tarpit suspicion increased by 2.
    client_elite.post("/submit", data={"_admin_confirm": "bot"})
    
    # 2. Measure next request time
    start_time = time.time()
    client_elite.get("/") 
    end_time = time.time()
    
    # Delay for score 2 should be 2^(2-1) = 2.0s
    duration = end_time - start_time
    assert duration >= 1.5 # Allow some buffer
