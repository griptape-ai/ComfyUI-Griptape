from griptape.drivers import AmazonSageMakerJumpstartEmbeddingDriver

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

default_model = ""
default_endpoint = "jumpstart-dft-..."
DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


class gtUIAmazonSageMakerJumpstartEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "OpenAI Compatible Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "model": ("STRING", {"default": default_model}),
                "endpoint": ("STRING", {"default": default_endpoint}),
                "aws_access_key_id_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_ACCESS_KEY_ID},
                ),
                "aws_secret_access_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_SECRET_ACCESS_KEY},
                ),
                "aws_default_region_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_DEFAULT_REGION},
                ),
            }
        )

        return inputs

    CATEGORY = "Griptape/Drivers/Embedding"

    def create(self, **kwargs):
        model = kwargs.get("model", default_model)
        endpoint = kwargs.get("endpoint", default_endpoint)

        params = {}

        if model:
            params["model"] = model
        if endpoint:
            params["endopoint"] = endpoint
        driver = AmazonSageMakerJumpstartEmbeddingDriver(**params)
        return (driver,)
