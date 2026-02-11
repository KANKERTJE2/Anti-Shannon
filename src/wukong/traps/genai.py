from faker import Faker
import random
from starlette.responses import JSONResponse
from starlette.requests import Request
import asyncio

fake = Faker()

class GenerativeTrap:
    """
    The Illusion: Generative AI Traps.
    Serves procedurally generated fake data to waste attacker time.
    """
    def __init__(self):
        self.trap_routes = ["/api/v1/users", "/api/v1/transactions", "/admin/logs"]

    async def is_trap(self, request: Request) -> bool:
        return request.url.path in self.trap_routes

    async def spring_trap(self, request: Request) -> JSONResponse:
        """
        Generates realistic but fake data based on the route.
        """
        path = request.url.path
        data = {}
        
        if "users" in path:
            data = [
                {
                    "id": fake.uuid4(),
                    "name": fake.name(),
                    "email": fake.email(),
                    "role": random.choice(["user", "editor", "viewer"]),
                    "last_login": fake.iso8601()
                }
                for _ in range(random.randint(10, 50))
            ]
        elif "transactions" in path:
             data = [
                {
                    "tx_id": fake.sha256(),
                    "amount": round(random.uniform(10.0, 5000.0), 2),
                    "currency": fake.currency_code(),
                    "status": random.choice(["pending", "completed", "failed"])
                }
                for _ in range(random.randint(5, 20))
            ]
        else:
             data = {"logs": [fake.sentence() for _ in range(20)]}
             
        # Add artificial delay to simulate processing and slow down the attacker
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        return JSONResponse({"data": data, "meta": {"page": 1, "total": 99999}})
