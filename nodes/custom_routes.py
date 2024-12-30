# pyright: reportMissingImports=false
from aiohttp import web
from server import PromptServer

from .get_version import get_version

# Import your route handlers here
from .utilities import get_models


def setup_routes():
    @PromptServer.instance.routes.post("/Griptape/get_models")
    async def get_models_endpoint(request):
        data = await request.json()
        engine = data.get("engine")
        base_ip = data.get("base_ip")
        port = data.get("port")
        models = get_models(engine, base_ip, port)
        return web.json_response(models)

    @PromptServer.instance.routes.get("/Griptape/get_version")
    async def get_version_endpoint(request):
        try:
            version = get_version()
            return web.json_response({"version": version})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)


# Call this function to set up all routes
def init_routes():
    try:
        setup_routes()
    except Exception as e:
        print(f"Failed to initialize custom routes: {e}")
    print("   \033[34m- Custom routes initialized.\033[0m")
