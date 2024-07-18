from griptape.drivers import OpenAiEmbeddingDriver

from .gtUIBaseDriver import gtUIBaseDriver

models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]


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
            }
        )

        return inputs

    CATEGORY = "Griptape/Drivers/Embedding"

    def create(self, **kwargs):
        model = kwargs.get("model", models[0])

        params = {}

        if model:
            params["model"] = model

        driver = OpenAiEmbeddingDriver(**params)
        return (driver,)
