from griptape.drivers import (
    OpenAiImageGenerationDriver,
)

from .BaseImageDriver import gtUIBaseImageGenerationDriver


class gtUIOpenAiImageGenerationDriver(gtUIBaseImageGenerationDriver):
    DESCRIPTION = "OpenAI Image Generation Driver"

    @classmethod
    def INPUT_TYPES(s):
        models = ["dall-e-3", "dall-e-2"]
        sizes = ["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"]

        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
                "size": (sizes, {"default": sizes[2]}),
            }
        )
        return inputs

    def adjust_size_based_on_model(self, model, size):
        # pick the approprite size based on the model
        if model == "dall-e-2":
            if size in ["1024x1792", "1792x1024"]:
                size = "1024x1024"
        if model == "dall-e-3":
            if size in ["256x256", "512x512"]:
                size = "1024x1024"
        return size

    def create(self, model, size, prompt):
        size = self.adjust_size_based_on_model(model, size)
        driver = OpenAiImageGenerationDriver(model=model, image_size=size)
        return (driver,)
