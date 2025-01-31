from typing import get_args

from griptape.drivers import OpenAiEmbeddingDriver
from openai.types import EmbeddingModel

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

models = get_args(EmbeddingModel)
# models = get_available_models("EmbeddingModel")
# models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
DEFAULT_MODEL = ""
if len(models) > 0:
    DEFAULT_MODEL = models[0]

DEFAULT_API_KEY = "OPENAI_API_KEY"


class gtUIOpenAiEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "OpenAI Embedding Driver"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["required"].update()
        inputs["optional"].update(
            {
                "embedding_model": (
                    models,
                    {
                        "default": DEFAULT_MODEL,
                        "tooltip": "Select the embedding model to use.",
                    },
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY,
                        "tooltip": "Enter the environment variable name that contains your API key, not the actual API key.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        model = kwargs.get("embedding_model", None)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))

        params = {}

        if model:
            params["model"] = model
        if api_key:
            params["api_key"] = api_key
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = OpenAiEmbeddingDriver(**params)
        return (driver,)
