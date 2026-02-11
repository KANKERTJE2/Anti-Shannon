from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from starlette.responses import RedirectResponse
import random
import time
import hmac
import hashlib

class RouteShifter:
    """
    The Mist: Dynamic Route Shifter.
    
    Strategy:
    1.  Protect sensitive routes (e.g. /admin) behind a dynamic token.
    2.  If token is missing/invalid, redirect to a honey-trap or 404.
    3.  Frontend needs to fetch the current token from a 'seed' endpoint.
    """
    def __init__(self, secret_key: str = "wukong-secret-key"):
        self.secret_key = secret_key.encode()
        self.protected_prefixes = ["/admin", "/api/private"]
    
    def _generate_token(self) -> str:
        # Token valid for 30 second windows
        timestamp = int(time.time() / 30)
        msg = f"{timestamp}".encode()
        return hmac.new(self.secret_key, msg, hashlib.sha256).hexdigest()[:16]

    async def check_route(self, request: Request) -> bool:
        """
        Returns True if request is allowed, False if it should be blocked.
        """
        path = request.url.path
        
        # Check if path is protected
        is_protected = any(path.startswith(p) for p in self.protected_prefixes)
        if not is_protected:
            return True
            
        # Check for dynamic token in query or header
        token = request.query_params.get("w_token") or request.headers.get("X-Wukong-Token")
        expected = self._generate_token()
        
        if token == expected:
            return True
            
        return False
        
    def get_seed_script(self) -> str:
        """
        Returns JS code to inject into frontend to auto-attach tokens.
        """
        return f"""
        <script>
        // Wukong Route Shifter Logic
        (function() {{
            async function getToken() {{
                // In a real app, this would fetch from a seed endpoint
                // For prototype, we simulate the HMAC logic or fetch from /wukong/token
                const response = await fetch('/wukong/token');
                const data = await response.json();
                return data.token;
            }}
            
            // Intercept fetch to add header
            const originalFetch = window.fetch;
            window.fetch = async function(url, options) {{
                if (url.includes('/admin') || url.includes('/api/private')) {{
                    const token = await getToken();
                    options = options || {{}};
                    options.headers = options.headers || {{}};
                    options.headers['X-Wukong-Token'] = token;
                }}
                return originalFetch(url, options);
            }};
        }})();
        </script>
        """
