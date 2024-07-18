import os

from griptape.drivers import VoyageAiEmbeddingDriver

from .BaseDriver import gtUIBaseDriver

default_api_key_env_var = "VOYAGE_API_KEY"


class gtUIVoyageAiEmbeddingDriver(gtUIBaseDriver):
    DESCRIPTION = "Voyage AI Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
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

        params = {}

        if api_key_env_var:
            params["api_key"] = os.getenv(api_key_env_var)
        driver = VoyageAiEmbeddingDriver(**params)
        return (driver,)
