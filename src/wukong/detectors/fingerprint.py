from starlette.requests import Request
import hashlib

class ClientFingerprinter:
    """
    The Identity Check: Fingerprints client based on headers.
    """
    def __init__(self):
        # Known signatures of bot libraries (simplified)
        # Real logic would need a database of JA3 or header order hashes
        self.bot_signatures = {
            # python-requests default headers often have specific order/values
            # This is illustrative; production needs robust header analysis
        }

    def fingerprint(self, request: Request) -> str:
        """
        Creates a hash of the header keys in order.
        """
        keys = sorted(request.headers.keys()) # Sorting destroys order info for simplistic servers, 
                                              # but Starlette headers are immutable dicts. 
                                              # To do this right, we'd need the raw ASGI scope headers list.
        # However, for a high-level prototype:
        raw_headers = request.scope['headers'] # list of [bytes, bytes]
        header_names = [h[0].decode().lower() for h in raw_headers]
        
        # Hash the ORDER of headers
        fingerprint = hashlib.md5("".join(header_names).encode()).hexdigest()
        return fingerprint

    async def is_bot(self, request: Request) -> bool:
        """
        Heuristic check for bots.
        """
        ua = request.headers.get("user-agent", "").lower()
        if "python" in ua or "curl" in ua or "wget" in ua:
            return True
            
        # Check for missing common browser headers
        common_headers = ["accept-language", "accept-encoding", "upgrade-insecure-requests"]
        missing_count = sum(1 for h in common_headers if h not in request.headers)
        
        if missing_count >= 2:
            return True
            
        return False
