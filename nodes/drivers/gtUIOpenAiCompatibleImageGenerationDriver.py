from griptape.drivers.image_generation.openai import OpenAiImageGenerationDriver

from .gtUIOpenAiImageGenerationDriver import gtUIOpenAiImageGenerationDriver

DEFAULT_API_KEY = "OPENAI_API_KEY"
models = ["dall-e-3", "dall-e-2"]
sizes = ["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"]
default_base_url = "https://api.openai.com/v1"


class gtUIOpenAiCompatibleImageGenerationDriver(gtUIOpenAiImageGenerationDriver):
    DESCRIPTION = "OpenAI Image Generation Driver"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "base_url": (
                    "STRING",
                    {
                        "default": default_base_url,
                        "tooltip": "The base URL for the OpenAI API",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        size_from_args = kwargs.get("size", sizes[2])
        model = kwargs.get("image_generation_model", models[0])
        size = self.adjust_size_based_on_model(model, size_from_args)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))
        base_url = kwargs.get("base_url", default_base_url)
        params = {
            "model": model,
            "image_size": size,
            "api_key": api_key,
            "base_url": base_url,
        }

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = OpenAiImageGenerationDriver(**params)
        return (driver,)
