from griptape.drivers import (
    AmazonBedrockImageGenerationDriver,
    BedrockTitanImageGenerationModelDriver,
)

from .BaseImageDriver import gtUIBaseImageGenerationDriver


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
