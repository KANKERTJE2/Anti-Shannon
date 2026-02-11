from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
import uvicorn
from wukong.middleware import WukongMiddleware

async def homepage(request):
    return JSONResponse({"message": "Welcome to the fortress"})

async def admin(request):
    return JSONResponse({"secret": "admin_panel_acccess"})

routes = [
    Route("/", homepage),
    Route("/admin", admin),
]

middleware = [
    Middleware(WukongMiddleware, enable_recon_shield=True, enable_probe_detection=True, enable_honey_traps=True)
]

app = Starlette(routes=routes, middleware=middleware)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
