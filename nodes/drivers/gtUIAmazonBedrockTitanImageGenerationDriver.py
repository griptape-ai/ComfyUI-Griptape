from griptape.drivers import (
    AmazonBedrockImageGenerationDriver,
    BedrockTitanImageGenerationModelDriver,
)

from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver

DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


class gtUIAmazonBedrockTitanImageGenerationDriver(gtUIBaseImageGenerationDriver):
    DESCRIPTION = "Amazon Bedrock Titan Image Generation Driver"

    @classmethod
    def INPUT_TYPES(s):
        sizes = ["512x512", "1024x1024"]
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "size": (sizes, {"default": sizes[0]}),
                "seed": ("INT", {"default": 10342349342}),
            }
        )
        inputs["optional"].update(
            {
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

    def create(self, size, seed, prompt):
        width, height = size.split("x")
        model_driver = BedrockTitanImageGenerationModelDriver()
        driver = AmazonBedrockImageGenerationDriver(
            image_generation_model_driver=model_driver,
            model="amazon.titan-image-generator-v1",
            image_width=int(width),
            image_height=int(height),
            seed=seed,
        )
        return (driver,)
