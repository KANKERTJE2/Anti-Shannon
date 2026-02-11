from starlette.requests import Request
from starlette.responses import Response, JSONResponse
import re

class ProbeDetector:
    """
    The Eye: Detects probe patterns from automated scanners.
    """
    def __init__(self):
        # Regex patterns for common Shannon/SQLi/XSS payloads
        self.attack_patterns = [
            r"UNION\s+SELECT",
            r"SLEEP\(\d+\)",
            r"<script>",
            r"javascript:",
            r"\.\./\.\./",  # Path traversal
            r"admin' --",
            r"1=1",
        ]
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.attack_patterns]

    def _has_pattern(self, text: str) -> bool:
        if not text:
            return False
        return any(p.search(text) for p in self.compiled_patterns)

    async def analyze(self, request: Request) -> bool:
        """
        Analyzes request query params and body for attack signatures.
        """
        # Check query parameters
        for _, value in request.query_params.items():
            if self._has_pattern(str(value)):
                return True
        
        # Check body (simplified for prototype)
        # In prod, stream body carefully to avoid DOS
        return False

    async def countermeasure(self, request: Request) -> Response:
        """
        Returns a deceptive response or block.
        """
        # Option: Infinite loading (Hold connection open)
        # Option: Fake successful SQLi response (Deception)
        return JSONResponse(
            {"error": "Internal Server Error", "details": "Database syntax error near 'UNION'"},
            status_code=500
        )
