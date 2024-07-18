from griptape.drivers import (
    AmazonBedrockImageQueryDriver,
    BedrockClaudeImageQueryModelDriver,
)

from .gtUIBaseImageQueryDriver import gtUIBaseImageQueryDriver

models = [
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
]


class gtUIAmazonBedrockClaudeImageQueryDriver(gtUIBaseImageQueryDriver):
    DESCRIPTION = "Griptape Azure OpenAI Image Query Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
            }
        )
        inputs["optional"].update({})

        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    def create(self, **kwargs):
        model = kwargs.get("model", models[0])

        params = {}

        if model:
            params["model"] = model
        params["image_query_model_driver"] = BedrockClaudeImageQueryModelDriver()
        try:
            driver = AmazonBedrockImageQueryDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None,)
