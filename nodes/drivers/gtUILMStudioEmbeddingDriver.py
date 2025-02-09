from griptape.drivers import OpenAiEmbeddingDriver

from .gtUIOpenAiCompatibleEmbeddingDriver import gtUIOpenAiCompatibleEmbeddingDriver

default_port = "1234"
default_base_url = "http://127.0.0.1"
DEFAULT_API_KEY = "lm_studio"


class gtUILMStudioEmbeddingDriver(gtUIOpenAiCompatibleEmbeddingDriver):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        del inputs["optional"]["api_key_env_var"]

        inputs["optional"].update(
            {
                "embedding_model": (
                    "STRING",
                    {"tooltip": "Select the embedding model to use."},
                ),
                "base_url": (
                    "STRING",
                    {
                        "default": default_base_url,
                        "tooltip": "The base URL for the embedding service.",
                    },
                ),
                "port": (
                    "STRING",
                    {
                        "default": default_port,
                        "tooltip": "The port number for the embedding service.",
                    },
                ),
                "use_native_tools": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Enable or disable the use of native tools.",
                        "label_on": "True (LLM-native tool calling)",
                        "label_off": "False (Griptape tool calling)",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY,
                        "tooltip": "API key for the embedding service. ",
                    },
                ),
            }
        )

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("embedding_model")
        base_url = kwargs.get("base_url", default_base_url)
        port = kwargs.get("port")
        api_key = kwargs.get("api_key")

        params = {
            "model": model,
            "base_url": f"{base_url}:{port}/v1/embeddings",
            "api_key": api_key,
        }

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        try:
            driver = OpenAiEmbeddingDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
