from griptape.drivers import OllamaEmbeddingDriver

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

default_port = "11434"
default_base_url = "http://127.0.0.1"


class gtUIOllamaEmbeddingDriver(gtUIBaseEmbeddingDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "base_url": (
                    "STRING",
                    {
                        "default": default_base_url,
                        "tooltip": "The base URL of the Ollama server",
                    },
                ),
                "port": (
                    "STRING",
                    {
                        "default": default_port,
                        "tooltip": "The port of the Ollama server",
                    },
                ),
            }
        )
        inputs["optional"].update(
            {
                "embedding_model": ((), {"tooltip": "The embedding model to use"}),
            }
        )

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("embedding_model", None)
        base_url = kwargs.get("base_url", default_base_url)
        port = kwargs.get("port", default_port)

        params = {}

        if model:
            params["model"] = model
        if base_url and port:
            params["host"] = f"{base_url}:{port}"

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        try:
            driver = OllamaEmbeddingDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
