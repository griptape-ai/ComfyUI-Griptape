from griptape.drivers import (
    AmazonBedrockImageGenerationDriver,
    BedrockStableDiffusionImageGenerationModelDriver,
)

from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver


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
