from typing import Any, Tuple

from griptape.drivers.embedding.openai import OpenAiEmbeddingDriver

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
DEFAULT_API_KEY_ENV_VAR = "OPENAI_API_KEY"
default_base_url = "https://api.openai.com/v1"


class gtUIOpenAiCompatibleEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "OpenAI Compatible Embedding Driver"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "embedding_model": (
                    "STRING",
                    {
                        "default": models[0],
                        "tooltip": "Select the embedding model to use.",
                    },
                ),
                "base_url": (
                    "STRING",
                    {
                        "default": default_base_url,
                        "tooltip": "Enter the base URL for the API.",
                    },
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV_VAR,
                        "tooltip": "Enter the environment variable name for the API key, not the actual API key.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        model = kwargs.get("embedding_model", models[0])
        base_url = kwargs.get("base_url", default_base_url)
        if kwargs.get("api_key"):
            api_key = kwargs.get("api_key")
        else:
            api_key = self.getenv(
                kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
            )

        params = {
            "model": model,
            "base_url": base_url,
            "api_key": api_key,
        }

        return params

    def create(self, **kwargs) -> Tuple[Any, ...]:
        params = self.build_params(**kwargs)
        driver = OpenAiEmbeddingDriver(**params)
        return (driver,)
