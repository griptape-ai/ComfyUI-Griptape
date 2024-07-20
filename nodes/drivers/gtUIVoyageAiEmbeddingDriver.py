from griptape.drivers import VoyageAiEmbeddingDriver

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

DEFAULT_API_KEY_ENV_VAR = "VOYAGE_API_KEY"


class gtUIVoyageAiEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "Voyage AI Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY_ENV_VAR},
                ),
            }
        )

        return inputs

    CATEGORY = "Griptape/Drivers/Embedding"

    def create(self, **kwargs):
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR)

        params = {}

        if api_key_env_var:
            params["api_key"] = self.getenv(api_key_env_var)
        driver = VoyageAiEmbeddingDriver(**params)
        return (driver,)
