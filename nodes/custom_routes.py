from aiohttp import web
from server import PromptServer

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


# Call this function to set up all routes
def init_routes():
    setup_routes()
    print("   \033[34m- Custom routes initialized.\033[0m")
