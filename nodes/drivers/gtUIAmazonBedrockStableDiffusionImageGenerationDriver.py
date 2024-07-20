from griptape.drivers import (
    AmazonBedrockImageGenerationDriver,
    BedrockStableDiffusionImageGenerationModelDriver,
)

from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver

DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


class gtUIAmazonBedrockStableDiffusionImageGenerationDriver(
    gtUIBaseImageGenerationDriver
):
    DESCRIPTION = "Amazon Bedrock Stable Diffusion Image Generation Driver"

    @classmethod
    def INPUT_TYPES(s):
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
        inputs["optional"].update(
            {
                "style_preset": (style_presets, {"default": style_presets[4]}),
                "width": (
                    "INT",
                    {"default": 512, "min": 64, "max": 2048, "step": 64},
                ),
                "height": (
                    "INT",
                    {"default": 512, "min": 64, "max": 2048, "step": 64},
                ),
                "seed": ("INT", {"default": 12345}),
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

    def create(self, style_preset, width, height, seed, prompt):
        if style_preset == "<None>":
            style_preset = None
        model_driver = BedrockStableDiffusionImageGenerationModelDriver(
            style_preset=style_preset,
        )
        driver = AmazonBedrockImageGenerationDriver(
            image_generation_model_driver=model_driver,
            model="stability.stable-diffusion-xl-v1",
            image_width=width,
            image_height=height,
            seed=seed,
        )
        return (driver,)
