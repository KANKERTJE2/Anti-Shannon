import os
import httpx
import logging
from fastapi import FastAPI, Request, Response
from starlette.middleware import Middleware
from starlette.background import BackgroundTask
from wukong.middleware import WukongMiddleware

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wukong.proxy")

# Configuration from Environment Variables
TARGET_URL = os.getenv("TARGET_URL", "http://localhost:8080")
DEBUG_MODE = os.getenv("WUKONG_DEBUG", "false").lower() == "true"

# Wukong Defense Flags
ENABLE_RECON_SHIELD = os.getenv("ENABLE_RECON_SHIELD", "true").lower() == "true"
ENABLE_ROUTE_SHIFTING = os.getenv("ENABLE_ROUTE_SHIFTING", "true").lower() == "true"
ENABLE_PROBE_DETECTION = os.getenv("ENABLE_PROBE_DETECTION", "true").lower() == "true"
ENABLE_HONEY_TRAPS = os.getenv("ENABLE_HONEY_TRAPS", "true").lower() == "true"
ENABLE_HONEY_TOKENS = os.getenv("ENABLE_HONEY_TOKENS", "true").lower() == "true"
ENABLE_VACUUM = os.getenv("ENABLE_VACUUM", "true").lower() == "true"
ENABLE_ML_ANOMALY = os.getenv("ENABLE_ML_ANOMALY", "false").lower() == "true"
ENABLE_FINGERPRINTING = os.getenv("ENABLE_FINGERPRINTING", "true").lower() == "true"
ENABLE_GENAI_TRAPS = os.getenv("ENABLE_GENAI_TRAPS", "true").lower() == "true"
ENABLE_HONEY_FIELDS = os.getenv("ENABLE_HONEY_FIELDS", "true").lower() == "true"
ENABLE_TARPIT = os.getenv("ENABLE_TARPIT", "true").lower() == "true"

app = FastAPI()

# Initialize HTTPX client for proxying
client = httpx.AsyncClient(base_url=TARGET_URL, timeout=None)

@app.on_event("shutdown")
async def shutdown_event():
    await client.aclose()

@app.middleware("http")
async def proxy_handler(request: Request, call_next):
    """
    Catch-all proxy handler that forwards requests to the target URL.
    """
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    
    # Extract body
    body = await request.body()
    
    # Forward original headers (excluding host to avoid target confusion)
    headers = dict(request.headers)
    headers.pop("host", None)
    
    # Prepare request
    proxy_request = client.build_request(
        method=request.method,
        url=url,
        headers=headers,
        content=body,
    )
    
    try:
        proxy_response = await client.send(proxy_request, stream=True)
    except httpx.ConnectError:
        return Response("Target server unreachable", status_code=502)

    return Response(
        content=await proxy_response.aread(),
        status_code=proxy_response.status_code,
        headers=dict(proxy_response.headers),
        background=BackgroundTask(proxy_response.aclose),
    )

# Wrap the proxy app with Wukong Middleware
# We add it as a Middleware to the FastAPI app so it intercepts everything
app.add_middleware(
    WukongMiddleware,
    enable_recon_shield=ENABLE_RECON_SHIELD,
    enable_route_shifting=ENABLE_ROUTE_SHIFTING,
    enable_probe_detection=ENABLE_PROBE_DETECTION,
    enable_honey_traps=ENABLE_HONEY_TRAPS,
    enable_honey_tokens=ENABLE_HONEY_TOKENS,
    enable_vacuum=ENABLE_VACUUM,
    enable_ml_anomaly=ENABLE_ML_ANOMALY,
    enable_fingerprinting=ENABLE_FINGERPRINTING,
    enable_genai_traps=ENABLE_GENAI_TRAPS,
    enable_honey_fields=ENABLE_HONEY_FIELDS,
    enable_tarpit=ENABLE_TARPIT,
)
