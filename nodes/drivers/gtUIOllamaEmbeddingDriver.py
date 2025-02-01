from griptape.drivers import DummyEmbeddingDriver, OllamaEmbeddingDriver

from ...py.griptape_settings import GriptapeSettings
from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

default_port = "11434"
default_base_url = "http://127.0.0.1"


class gtUIOllamaEmbeddingDriver(gtUIBaseEmbeddingDriver):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "base_url": (
                    "STRING",
                    {
                        "default": cls.get_default_url(),
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
                "embedding_model": (
                    (),
                    {"tooltip": "The embedding model to use"},
                ),
            }
        )

        return inputs

    @classmethod
    def VALIDATE_INPUTS(cls, embedding_model):
        if not embedding_model:
            return """
            
                    [GRIPTAPE WARNING] No embedding model has been supplied.

                    In order for Griptape to create an embedding driver, an embedding model must be specified.
                    
                    If there are no embedding models available, you may need to pull one from the registry.

                    For example, open a terminal and run:

                    ollama pull nomic-embed-text

                    Once it's finished, refresh your browser and you should see it in the list of available models.
                    """
        return True

        return embedding_model in ["nomic-embed-text", "nomic-embed-text-v1.5"]

    @classmethod
    def get_default_url(cls):
        settings = GriptapeSettings()
        default_url = settings.get_settings_key("ollama_base_url")
        return default_url

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("embedding_model", None)
        base_url = kwargs.get(
            "base_url",
            self.get_default_url(),
        )
        port = kwargs.get("port", default_port)

        params = {}

        if model:
            params["model"] = model
        if base_url and port:
            params["host"] = f"{base_url}:{port}"

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        if "model" not in params:
            driver = DummyEmbeddingDriver()
        try:
            driver = OllamaEmbeddingDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
