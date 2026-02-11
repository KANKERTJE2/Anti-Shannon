import asyncio
import time
import logging
from typing import Dict

logger = logging.getLogger("wukong.tarpit")

class TarPit:
    """
    The Tar Pit: Slowly drains AI resources by delaying responses.
    """
    def __init__(self, max_delay: float = 30.0):
        self.max_delay = max_delay
        # Maps IP -> current suspicion count
        self.suspicion_scores: Dict[str, int] = {}

    async def apply_delay(self, ip: str):
        """
        Applies an exponential delay based on the IP's suspicion score.
        delay = 2^(score - 1)
        """
        score = self.suspicion_scores.get(ip, 0)
        if score <= 0:
            return

        # Calculate exponential delay
        delay = min(2.0 ** (score - 1), self.max_delay)
        
        logger.warning(f"⏳ TAR-PIT: Delaying request from {ip} for {delay:.2f}s (Score: {score})")
        await asyncio.sleep(delay)

    def increase_suspicion(self, ip: str, amount: int = 1):
        """
        Increases the suspicion score for an IP.
        """
        self.suspicion_scores[ip] = self.suspicion_scores.get(ip, 0) + amount
        logger.info(f"📈 TAR-PIT: Suspicion increased for {ip}. Current score: {self.suspicion_scores[ip]}")

    def reset_suspicion(self, ip: str):
        """
        Resets the suspicion score for an IP.
        """
        if ip in self.suspicion_scores:
            del self.suspicion_scores[ip]
