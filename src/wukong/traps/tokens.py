import secrets
import logging
from starlette.requests import Request

logger = logging.getLogger("wukong.honeytoken")

class HoneyTokenGenerator:
    """
    The Deception: Honeytoken Generator & Monitor.
    Generates fake credentials (JWTs, API Keys) and monitors their usage.
    """
    # Shared state for prototype (in prod use Redis)
    _active_honeytokens = set()

    def __init__(self):
        pass
        
    def generate_token(self, context: str = "admin") -> str:
        """
        Generates a convincing-looking fake token.
        """
        # Fake JWT structure: header.payload.signature
        header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" # {"alg":"HS256","typ":"JWT"}
        payload = rf"eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJyb2xlIjoi{context}" # payload with role
        signature = secrets.token_urlsafe(32)
        token = f"{header}.{payload}.{signature}"
        
        self._active_honeytokens.add(token)
        return token

    def is_honeytoken(self, token: str) -> bool:
        return token in self._active_honeytokens

    async def log_trap_trigger(self, request: Request, token: str):
        """
        Log the event when a honeytoken is used. 
        In production, this would ban the IP.
        """
        client_ip = request.client.host if request.client else "unknown"
        logger.critical(f"🚨 HONEYTOKEN TRIGGERED! Client IP: {client_ip} used token: {token}")
        # Logic to ban IP would go here
