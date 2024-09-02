import os

from griptape.drivers import CohereRerankDriver

from .gtUIBaseRerankDriver import gtUIBaseRerankDriver

DEFAULT_API_KEY_ENV_VAR = "COHERE_API_KEY"
models = ["rerank-english-v3.0", "rerank-multilingual-v3.0"]


class gtUICohereRerankDriver(gtUIBaseRerankDriver):
    DESCRIPTION = "Cohere Rerank Driver"

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
                "top_n": (
                    "INT",
                    {"default": 5},
                ),
                "api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY_ENV_VAR},
                ),
            }
        )

        return inputs

    def create(self, **kwargs):
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        model = kwargs.get("models", models[0])
        top_n = kwargs.get("top_n", 5)
        params = {}

        if model:
            params["model"] = model
        if api_key_env_var:
            params["api_key"] = os.getenv(api_key_env_var)
        params["top_n"] = top_n

        driver = CohereRerankDriver(**params)
        return (driver,)