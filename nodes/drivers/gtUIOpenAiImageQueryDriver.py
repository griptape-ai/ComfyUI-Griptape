import os

from griptape.drivers import OpenAiImageQueryDriver

from .gtUIBaseImageQueryDriver import gtUIBaseImageQueryDriver

models = [
    "gpt-4o",
    "gpt-4-vision-preview",
]

default_api_key_env = "OPENAI_API_KEY"


class gtUIOpenAiImageQueryDriver(gtUIBaseImageQueryDriver):
    DESCRIPTION = "Griptape OpenAI Image Query Driver"

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
            driver = OpenAiImageQueryDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None,)
