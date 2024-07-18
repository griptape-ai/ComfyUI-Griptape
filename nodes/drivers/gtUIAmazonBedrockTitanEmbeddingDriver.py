from griptape.drivers import AmazonBedrockTitanEmbeddingDriver

from .gtUIBaseDriver import gtUIBaseDriver

models = [
    "amazon.titan-text-premier-v1:0",
    "amazon.titan-text-express-v1",
    "amazon.titan-text-lite-v1",
]


class gtUIAmazonBedrockTitanEmbeddingDriver(gtUIBaseDriver):
    DESCRIPTION = "Amazon Bedrock Titan Embedding Driver"

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

        driver = AmazonBedrockTitanEmbeddingDriver(**params)
        return (driver,)
