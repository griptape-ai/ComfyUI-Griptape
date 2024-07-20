from griptape.drivers import (
    OpenAiImageGenerationDriver,
)

from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver

DEFAULT_API_KEY = "OPENAI_API_KEY"
models = ["dall-e-3", "dall-e-2"]
sizes = ["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"]


class gtUIOpenAiImageGenerationDriver(gtUIBaseImageGenerationDriver):
    DESCRIPTION = "OpenAI Image Generation Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
                "size": (sizes, {"default": sizes[2]}),
            }
        )
        inputs["optional"].update(
            {
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY}),
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

    def create(self, model, size, prompt, **kwargs):
        size_from_args = kwargs.get("size", sizes[2])
        model = kwargs.get("model", models[0])
        size = self.adjust_size_based_on_model(model, size_from_args)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))

        params = {}
        if model:
            params["model"] = model
        if size:
            params["size"] = size
        if api_key:
            params["api_key"] = api_key
        driver = OpenAiImageGenerationDriver(**params)
        return (driver,)
