import logging
import time
from typing import Dict, Set

logger = logging.getLogger("wukong.vacuum")

class VulnerabilityVacuum:
    """
    The Iron Body: Auto-Patching & Vulnerability Vacuum.
    When a probe is detected, this module 'hardens' the route or IP context
    dynamically, effectively patching the vulnerability in real-time.
    """
    def __init__(self):
        # Maps IP -> {score, blocked_until}
        self.ip_reputation: Dict[str, dict] = {}
        # Maps Route -> Stricter Mode Enabled (True/False)
        self.hardened_routes: Set[str] = set()

    async def report_probe(self, ip: str, route: str, severity: int = 1):
        """
        Reports a probe attempt. Accumulates risk score.
        If threshold exceeded, triggers hardening.
        """
        current_time = time.time()
        
        # IP Reputation Logic
        if ip not in self.ip_reputation:
            self.ip_reputation[ip] = {"score": 0, "blocked_until": 0}
        
        details = self.ip_reputation[ip]
        if current_time < details["blocked_until"]:
            return  # Already blocked
            
        details["score"] += severity
        
        # Threshold for blocking IP
        if details["score"] >= 5:
            duration = 60 * 5  # 5 minutes block
            details["blocked_until"] = current_time + duration
            logger.warning(f"🛡️ VACUUM: IP {ip} blocked for {duration}s due to probe threshold.")

        # Route Hardening Logic
        # If a specific route sees multiple attacks from different IPs, harden it globally
        # (For prototype, we simplify this to just tracking the concept)
        self.hardened_routes.add(route)
        logger.info(f"🔧 VACUUM: Route {route} verified as attack target. Hardening enabled.")

    def is_blocked(self, ip: str) -> bool:
        """Returns True if IP is currently blocked."""
        if ip not in self.ip_reputation:
            return False
        
        details = self.ip_reputation[ip]
        if details["blocked_until"] > time.time():
            return True
            
        return False

    def is_route_hardened(self, route: str) -> bool:
        """Returns True if route is in hardened mode (e.g. strict validation)."""
        return route in self.hardened_routes
