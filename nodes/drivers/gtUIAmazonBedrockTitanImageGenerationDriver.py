from griptape.drivers import (
    AmazonBedrockImageGenerationDriver,
    BedrockTitanImageGenerationModelDriver,
)

from ..config.gtUIAmazonBedrockSession import start_session
from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver

DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"

models = ["amazon.titan-image-generator-v1", "amazon.titan-image-generator-v2"]


class gtUIAmazonBedrockTitanImageGenerationDriver(gtUIBaseImageGenerationDriver):
    DESCRIPTION = "Amazon Bedrock Titan Image Generation Driver"

    @classmethod
    def INPUT_TYPES(cls):
        sizes = ["512x512", "1024x1024"]
        inputs = super().INPUT_TYPES()

        # Get the base required and optional inputs
        base_required_inputs = inputs["required"]
        base_optional_inputs = inputs["optional"]

        # Add the base required inputs to the inputs
        inputs["required"].update(base_required_inputs)

        # Add the optional inputs
        inputs["optional"].update(base_optional_inputs)

        inputs["optional"].update(
            {
                "image_generation_model": (
                    "STRING",
                    {
                        "default": "amazon.titan-image-generator-v1",
                        "tooltip": "Select the image generation model to use.",
                    },
                ),
                "size": (
                    sizes,
                    {
                        "default": sizes[0],
                        "tooltip": "Choose the size of the generated image.",
                    },
                ),
                "seed": (
                    "INT",
                    {
                        "default": 10342349342,
                        "tooltip": "Set the seed for random number generation.",
                    },
                ),
                "aws_access_key_id_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_AWS_ACCESS_KEY_ID,
                        "tooltip": "Enter the name of the environment variable for your AWS_ACCESS_KEY_ID, not your actual key.",
                    },
                ),
                "aws_secret_access_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_AWS_SECRET_ACCESS_KEY,
                        "tooltip": "Enter the name of the environment variable for your AWS_SECRET_ACCESS_KEY, not your actual key.",
                    },
                ),
                "aws_default_region_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_AWS_DEFAULT_REGION,
                        "tooltip": "Enter the name of the environment variable for your AWS_DEFAULT_REGION, not your actual region.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        model = kwargs.get("image_generation_model", "amazon.titan-image-generator-v1")
        size = kwargs.get("size", "512x512")
        width, height = size.split("x")

        seed = kwargs.get("seed", 10342349342)
        api_key = self.getenv(
            kwargs.get("aws_access_key_id_env_var", DEFAULT_AWS_ACCESS_KEY_ID)
        )
        secret_access_key = self.getenv(
            kwargs.get("aws_secret_access_key_env_var", DEFAULT_AWS_SECRET_ACCESS_KEY)
        )
        region_name = self.getenv(
            kwargs.get("aws_default_region_env_var", DEFAULT_AWS_DEFAULT_REGION)
        )
        params = {
            "image_generation_model_driver": BedrockTitanImageGenerationModelDriver(),
            "model": model,
            "image_width": int(width),
            "image_height": int(height),
            "seed": seed,
            "aws_access_key_id": api_key,
            "aws_secret_access_key": secret_access_key,
            "region_name": region_name,
        }

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        start_session(
            aws_access_key_id=params.get("aws_access_key_id", None),
            aws_secret_access_key=params.get("aws_secret_access_key", None),
            region_name=params.get("region_name", None),
        )
        params.pop("aws_access_key_id")
        params.pop("aws_secret_access_key")
        params.pop("region_name")

        driver = AmazonBedrockImageGenerationDriver(**params)
        return (driver,)
