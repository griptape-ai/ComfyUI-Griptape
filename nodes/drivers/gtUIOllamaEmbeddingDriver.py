from griptape.drivers import OllamaEmbeddingDriver

from ..utilities import get_models
from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

default_port = "11434"
default_base_url = "http://127.0.0.1"
models = get_models("ollama", default_base_url, default_port)
if len(models) == 0:
    models.append("")


class gtUIOllamaEmbeddingDriver(gtUIBaseEmbeddingDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": ((), {}),
                "base_url": ("STRING", {"default": default_base_url}),
                "port": ("STRING", {"default": default_port}),
            }
        )
        inputs["optional"].update({})

        return inputs

    FUNCTION = "create"

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
            driver = OllamaEmbeddingDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
