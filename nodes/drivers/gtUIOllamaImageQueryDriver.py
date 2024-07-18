from griptape.drivers import OllamaPromptDriver

from ..utilities import get_ollama_models
from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = get_ollama_models()
models.append("")
default_port = "11434"
default_base_url = "http://127.0.0.1"


class gtUIOllamaImageQueryDriver(gtUIBasePromptDriver):
    DESCRIPTION = "Driver for Ollama's image query model. Doesn't work with all models."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": ([""], {"default": ""}),
                "base_url": ("STRING", {"default": default_base_url}),
                "port": ("STRING", {"default": default_port}),
            }
        )
        inputs["optional"].update({})

        del inputs["optional"]["stream"]
        del inputs["optional"]["temperature"]
        del inputs["optional"]["max_attempts_on_fail"]
        del inputs["optional"]["seed"]

        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Drivers/Image Query"

    def create(self, **kwargs):
        model = kwargs.get("model", None)
        base_url = kwargs.get("base_url", default_base_url)
        port = kwargs.get("port", default_port)

        params = {}

        if model:
            params["model"] = model
        if base_url and port:
            params["host"] = f"{base_url}:{port}"

        try:
            driver = OllamaPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
