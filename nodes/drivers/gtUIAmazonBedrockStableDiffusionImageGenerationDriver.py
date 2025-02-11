from griptape.drivers.image_generation.amazon_bedrock import (
    AmazonBedrockImageGenerationDriver,
)
from griptape.drivers.image_generation_model.bedrock_stable_diffusion import (
    BedrockStableDiffusionImageGenerationModelDriver,
)

from ..config.gtUIAmazonBedrockSession import start_session
from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver

DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


class gtUIAmazonBedrockStableDiffusionImageGenerationDriver(
    gtUIBaseImageGenerationDriver
):
    DESCRIPTION = "Amazon Bedrock Stable Diffusion Image Generation Driver"

    @classmethod
    def INPUT_TYPES(cls):
        style_presets = [
            "<None>",
            "3d-model",
            "analog-film",
            "anime",
            "cinematic",
            "comic-book",
            "digital-art",
            "enhance",
            "fantasy-art",
            "isometric",
            "line-art",
            "low-poly",
            "modeling-compound",
            "neon-punk",
            "origami",
            "photographic",
            "pixel-art",
            "tile-texture",
        ]
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
                "style_preset": (
                    style_presets,
                    {
                        "default": style_presets[4],
                        "tooltip": "Select a style preset for the image generation.",
                    },
                ),
                "width": (
                    "INT",
                    {
                        "default": 512,
                        "min": 64,
                        "max": 2048,
                        "step": 64,
                        "tooltip": "Specify the width of the generated image.",
                    },
                ),
                "height": (
                    "INT",
                    {
                        "default": 512,
                        "min": 64,
                        "max": 2048,
                        "step": 64,
                        "tooltip": "Specify the height of the generated image.",
                    },
                ),
                "seed": (
                    "INT",
                    {
                        "default": 12345,
                        "tooltip": "Set the seed for random number generation to ensure reproducibility.",
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
        style_preset = kwargs.get("style_preset", None)
        width = kwargs.get("width", 512)
        height = kwargs.get("height", 512)
        seed = kwargs.get("seed", 12345)
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
            "image_generation_model_driver": BedrockStableDiffusionImageGenerationModelDriver(
                style_preset=style_preset,
            ),
            "model": "stability.stable-diffusion-xl-v1",
            "image_width": width,
            "image_height": height,
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
