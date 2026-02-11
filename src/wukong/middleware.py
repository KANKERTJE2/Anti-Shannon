import logging
import typing
import asyncio
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse, JSONResponse

from wukong.defense.recon import ReconShield
from wukong.defense.shifting import RouteShifter
from wukong.detectors.probe import ProbeDetector
from wukong.traps.honey import HoneyTrap
from wukong.traps.tokens import HoneyTokenGenerator
from wukong.defense.vacuum import VulnerabilityVacuum
from wukong.detectors.anomaly import AnomalyDetector
from wukong.detectors.fingerprint import ClientFingerprinter
from wukong.traps.genai import GenerativeTrap
from wukong.traps.honeyforms import HoneyFieldManager
from wukong.defense.tarpit import TarPit

logger = logging.getLogger("wukong")

class WukongMiddleware:
    """
    The Iron Body of Wukong: Elite Edition.
    """
    def __init__(
        self,
        app: ASGIApp,
        enable_recon_shield: bool = True,
        enable_route_shifting: bool = True,
        enable_probe_detection: bool = True,
        enable_honey_traps: bool = True,
        enable_honey_tokens: bool = True,
        enable_vacuum: bool = True,
        enable_ml_anomaly: bool = False,
        enable_fingerprinting: bool = False,
        enable_genai_traps: bool = False,
        enable_honey_fields: bool = True,
        enable_tarpit: bool = True,
    ) -> None:
        self.app = app
        self.recon_shield = ReconShield() if enable_recon_shield else None
        self.route_shifter = RouteShifter() if enable_route_shifting else None
        self.probe_detector = ProbeDetector() if enable_probe_detection else None
        self.honey_trap = HoneyTrap() if enable_honey_traps else None
        self.honey_token_gen = HoneyTokenGenerator() if enable_honey_tokens else None
        self.vacuum = VulnerabilityVacuum() if enable_vacuum else None
        self.anomaly_detector = AnomalyDetector() if enable_ml_anomaly else None
        self.fingerprinter = ClientFingerprinter() if enable_fingerprinting else None
        self.genai_trap = GenerativeTrap() if enable_genai_traps else None
        self.honey_fields = HoneyFieldManager() if enable_honey_fields else None
        self.tarpit = TarPit() if enable_tarpit else None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        client_ip = request.client.host if request.client else "unknown"

        # -3. Tar Pit (Resource Drain)
        if self.tarpit:
            await self.tarpit.apply_delay(client_ip)

        # -2. Check for Global Block (Vacuum)
        if self.vacuum and self.vacuum.is_blocked(client_ip):
             response = PlainTextResponse("Access Denied", status_code=403)
             await response(scope, receive, send)
             return

        # -1.75 Honey Form Check (The Lure)
        # We need to buffer the body if we read it, so the app can read it too.
        if request.method == "POST" and self.honey_fields:
            # Buffer the body
            body = await request.body()
            
            # Use a dummy request/form check that doesn't consume the main stream
            # (or rather, we already consumed it, so we'll need to pass it back)
            if await self._check_honey_fields(request, body):
                if self.vacuum:
                     await self.vacuum.report_probe(client_ip, "honeyfield", severity=5)
                if self.tarpit:
                     self.tarpit.increase_suspicion(client_ip, amount=2)
                
                response = JSONResponse({"error": "Validation Failed", "message": "Hidden field detected"}, status_code=400)
                await response(scope, receive, send)
                return

            # Reconstruct receive for the app
            async def receive_with_body():
                return {"type": "http.request", "body": body, "more_body": False}
            
            receive = receive_with_body


        # -1.5 Fingerprint Check (The Identity)
        if self.fingerprinter and await self.fingerprinter.is_bot(request):
            logger.warning(f"🤖 Fingerprint: Bot detected from {client_ip}")
            if self.vacuum:
                 await self.vacuum.report_probe(client_ip, "bot_fingerprint", severity=1)
            if self.tarpit:
                 self.tarpit.increase_suspicion(client_ip, amount=1)

        # -1.25 ML Anomaly Check (The Gut Feeling)
        if self.anomaly_detector and self.anomaly_detector.is_trained:
            try:
                body_len = int(request.headers.get("content-length", 0))
            except:
                body_len = 0
            
            features = self.anomaly_detector._extract_features(request, body_len)
            prediction = self.anomaly_detector.predict(features)
            
            if prediction == -1:
                logger.warning(f"🧠 ML: Anomaly detected from {client_ip}")
                if self.vacuum:
                     await self.vacuum.report_probe(client_ip, "anomaly", severity=2)
                if self.tarpit:
                     self.tarpit.increase_suspicion(client_ip, amount=1)

        # -1. Check for Honeytokens in Headers (The Tripwire)
        if self.honey_token_gen:
            auth_header = request.headers.get("Authorization")
            if auth_header and "Bearer" in auth_header:
                try:
                    token = auth_header.split(" ")[1]
                    if self.honey_token_gen.is_honeytoken(token):
                        logger.critical(f"🚨 BLOCKED ATTACKER IP: {client_ip}")
                        await self.honey_token_gen.log_trap_trigger(request, token)
                        if self.vacuum:
                            await self.vacuum.report_probe(client_ip, "honeytoken", severity=10)
                        if self.tarpit:
                            self.tarpit.increase_suspicion(client_ip, amount=5)
                        
                        response = JSONResponse({"error": "Unauthorized"}, status_code=401)
                        await response(scope, receive, send)
                        return
                except IndexError:
                    pass

        # 0. Route Shifting (The Maze)
        if self.route_shifter:
            is_allowed = await self.route_shifter.check_route(request)
            if not is_allowed:
                if self.tarpit:
                     self.tarpit.increase_suspicion(client_ip, amount=1)
                
                if self.genai_trap:
                     response = await self.genai_trap.spring_trap(request)
                     await response(scope, receive, send)
                     return

                if self.honey_trap:
                    response = await self.honey_trap.spring_trap(request)
                    await response(scope, receive, send)
                    return
                
                response = PlainTextResponse("Not Found", status_code=404)
                await response(scope, receive, send)
                return

        # 1. Detection Phase (The Eye)
        if self.probe_detector and await self.probe_detector.analyze(request):
            if self.vacuum:
                await self.vacuum.report_probe(client_ip, request.url.path, severity=2)
            if self.tarpit:
                 self.tarpit.increase_suspicion(client_ip, amount=2)
            
            response = await self.probe_detector.countermeasure(request)
            await response(scope, receive, send)
            return

        # 2. Trap Phase (The Mist)
        if self.genai_trap and await self.genai_trap.is_trap(request):
            if self.vacuum:
                 await self.vacuum.report_probe(client_ip, request.url.path, severity=1)
            response = await self.genai_trap.spring_trap(request)
            await response(scope, receive, send)
            return

        if self.honey_trap and await self.honey_trap.is_trap(request):
            if self.vacuum:
                 await self.vacuum.report_probe(client_ip, request.url.path, severity=1)
            response = await self.honey_trap.spring_trap(request)
            await response(scope, receive, send)
            return

        # 3. Defense Phase (The Shield) - Modify Response
        async def defensive_send(message: typing.MutableMapping[str, typing.Any]) -> None:
            if message["type"] == "http.response.body":
                body = message.get("body", b"")
                if body:
                    # Apply ReconShield
                    if self.recon_shield:
                        body = self.recon_shield.obfuscate(body)
                    
                    # Apply HoneyForm injection
                    if self.honey_fields:
                        body = self.honey_fields.inject_traps(body)
                        
                    message["body"] = body
            
            await send(message)

        await self.app(scope, receive, defensive_send)

    async def _check_honey_fields(self, request: Request, body: bytes) -> bool:
        """Helper to check honey fields from buffered body."""
        # Simple check for now: is any trap field name in the raw body?
        # A real implementation would parse the multipart/form-data properly.
        # But for this prototype, checking the raw bytes for "field_name=value" is enough.
        content = body.decode("utf-8", errors="ignore")
        for field in self.honey_fields.trap_fields:
            if f"{field}=" in content and len(content.split(f"{field}=")[1].split("&")[0]) > 0:
                return True
        return False

