import os

from griptape.drivers import CohereEmbeddingDriver

from .gtUIBaseDriver import gtUIBaseDriver

default_api_key_env_var = "COHERE_API_KEY"
models = ["embed-english-v3.0", "embed-multilingual-v3.0"]
input_types = ["search_query", "search_document", "classification"]


class gtUICohereEmbeddingDriver(gtUIBaseDriver):
    DESCRIPTION = "Cohere Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "models": (
                    models,
                    {"default": models[0]},
                ),
                "input_types": (
                    input_types,
                    {"default": input_types[0]},
                ),
                "api_key_env_var": (
                    "STRING",
                    {"default": default_api_key_env_var},
                ),
            }
        )

        return inputs

    CATEGORY = "Griptape/Drivers/Embedding"

    def create(self, **kwargs):
        api_key_env_var = kwargs.get("api_key_env_var", default_api_key_env_var)
        model = kwargs.get("models", models[0])
        input_type = kwargs.get("input_types", input_types[0])
        params = {}

        if model:
            params["model"] = model
        if input_type:
            params["input_type"] = input_type
        if api_key_env_var:
            params["api_key"] = os.getenv(api_key_env_var)
        driver = CohereEmbeddingDriver(**params)
        return (driver,)
