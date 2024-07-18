import os

from griptape.drivers import AnthropicImageQueryDriver

from .gtUIBaseImageQueryDriver import gtUIBaseImageQueryDriver

models = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

default_api_key_env = "ANTHROPIC_API_KEY"


class gtUIAnthropicImageQueryDriver(gtUIBaseImageQueryDriver):
    DESCRIPTION = "Griptape Anthropic Image Query Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
                "api_key_env_var": ("STRING", {"default": default_api_key_env}),
            }
        )
        inputs["optional"].update({})

        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    def create(self, **kwargs):
        api_key_env_var = kwargs.get("api_key_env_var", default_api_key_env)
        model = kwargs.get("model", models[0])

        params = {}

        if api_key_env_var:
            params["api_key"] = os.getenv(api_key_env_var)
        if model:
            params["model"] = model

        try:
            driver = AnthropicImageQueryDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None,)
