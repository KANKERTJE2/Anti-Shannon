from starlette.requests import Request
from starlette.responses import Response, JSONResponse, PlainTextResponse
import random
import asyncio

class HoneyTrap:
    """
    The Trap: Handles honey-routes and deceptive endpoints.
    """
    def __init__(self):
        self.honey_routes = [
            "/admin/debug",
            "/api/v2/test",
            "/backup/config.json",
        ]

    async def is_trap(self, request: Request) -> bool:
        return request.url.path in self.honey_routes

    async def spring_trap(self, request: Request) -> Response:
        """
        Springs the trap on the attacker.
        Strategy: Resource Exhaustion (The "Infinite Scroll" of JSON)
        """
        # Simulate a slow, heavy response to waste AI context window
        # In a real async framework, we'd stream this slowly.
        
        junk_data = {
            "status": "success",
            "data": [
                {"id": i, "hash": str(hash(i)*100)} for i in range(1000)
            ],
            "debug_trace": "x" * 5000  # Junk filler
        }
        
        # Simulate processing delay
        # await asyncio.sleep(2) 
        
        return JSONResponse(junk_data)
