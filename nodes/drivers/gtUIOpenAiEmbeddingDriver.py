from griptape.drivers import OpenAiEmbeddingDriver

from .gtUIBaseDriver import gtUIBaseDriver

models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]

DEFAULT_API_KEY = "OPENAI_API_KEY"


class gtUIOpenAiEmbeddingDriver(gtUIBaseDriver):
    DESCRIPTION = "OpenAI Embedding Driver"

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
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY}),
            }
        )

        return inputs

    CATEGORY = "Griptape/Drivers/Embedding"

    def create(self, **kwargs):
        model = kwargs.get("model", models[0])
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))

        params = {}

        if model:
            params["model"] = model
        if api_key:
            params["api_key"] = api_key
        driver = OpenAiEmbeddingDriver(**params)
        return (driver,)
