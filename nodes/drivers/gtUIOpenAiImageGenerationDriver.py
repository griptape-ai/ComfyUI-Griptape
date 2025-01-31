from typing import get_args

from griptape.drivers import OpenAiImageGenerationDriver
from openai.types import ImageModel

from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver

DEFAULT_API_KEY = "OPENAI_API_KEY"
# models = ["dall-e-3", "dall-e-2"]
# models = get_available_models("ImageModel")
models = get_args(ImageModel)
DEFAULT_MODEL = "dall-e-3"

sizes = ["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"]


class gtUIOpenAiImageGenerationDriver(gtUIBaseImageGenerationDriver):
    DESCRIPTION = "OpenAI Image Generation Driver"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "image_generation_model": (
                    models,
                    {
                        "default": DEFAULT_MODEL,
                        "tooltip": "Select the image generation model.",
                    },
                ),
                "size": (
                    sizes,
                    {"default": sizes[2], "tooltip": "Select the desired image size."},
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY,
                        "tooltip": "Enter the environment variable name for the API key, not the actual API key.",
                    },
                ),
            }
        )

        return inputs

    def adjust_size_based_on_model(self, model, size):
        # pick the appropriate size based on the model
        if model == "dall-e-2":
            if size in ["1024x1792", "1792x1024"]:
                size = "1024x1024"
        if model == "dall-e-3":
            if size in ["256x256", "512x512"]:
                size = "1024x1024"
        return size

    def build_params(self, **kwargs):
        size_from_args = kwargs.get("size", sizes[2])
        model = kwargs.get("image_generation_model", DEFAULT_MODEL)
        size = self.adjust_size_based_on_model(model, size_from_args)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))

        params = {}

        if model:
            params["model"] = model
        if size:
            params["image_size"] = size
        if api_key:
            params["api_key"] = api_key

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = OpenAiImageGenerationDriver(**params)
        return (driver,)
