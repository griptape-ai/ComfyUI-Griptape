from griptape.drivers import OpenAiEmbeddingDriver

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
DEFAULT_API_KEY_ENV_VAR = "OPENAI_API_KEY"
default_base_url = "https://api.openai.com/v1"


class gtUIOpenAiCompatibleEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "OpenAI Compatible Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "model": (
                    models,
                    {"default": models[0]},
                ),
                "base_url": (
                    "STRING",
                    {"default": default_base_url},
                ),
                "api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY_ENV_VAR},
                ),
            }
        )

        return inputs

    CATEGORY = "Griptape/Drivers/Embedding"

    def create(self, **kwargs):
        model = kwargs.get("model", models[0])
        base_url = kwargs.get("base_url", default_base_url)
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR)

        params = {}

        if model:
            params["model"] = model
        if base_url:
            params["base_url"] = base_url
        if api_key_env_var:
            params["api_key"] = self.getenv(api_key_env_var)
        driver = OpenAiEmbeddingDriver(**params)
        return (driver,)
