import random
import re

class ReconShield:
    """
    The Mist Layer: Anti-Reconnaissance Shield.
    Injects dynamic noise into responses to confuse static analysis agents.
    """
    def __init__(self):
        self.noise_comments = [
            "<!-- DEBUG: User session tracking enabled -->",
            "<!-- TODO: Remove admin bypass in production -->",
            "<!-- API v2 endpoint: /api/v2/admin_test -->",
            "<!-- Legacy auth flow: check /old-login -->",
        ]

    def obfuscate(self, body: bytes) -> bytes:
        """
        Injects random comments into HTML/JSON responses.
        For JSON, adds a '_debug_metadata' field with junk.
        """
        try:
            content = body.decode("utf-8")
        except UnicodeDecodeError:
            return body  # Binary content, skip
        
        if b"<html" in body or b"<body" in body:
            injection = random.choice(self.noise_comments)
            # Inject before </body>
            return body.replace(b"</body>", f"{injection}\n".encode("utf-8") + b"</body>")
            
        return body
