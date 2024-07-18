import os

from griptape.drivers import HuggingFaceHubPromptDriver

from .BasePromptDriver import gtUIBasePromptDriver

default_model = "HuggingFaceH4/zephyr-7b-beta"


class gtUIHuggingFaceHubPromptDriver(gtUIBasePromptDriver):
    DESCRIPTION = "Hugging Face Hub Prompt Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": ("STRING", {"default": default_model}),
            }
        )
        inputs["optional"].update({})

        del inputs["optional"]["stream"]
        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Drivers/Prompt"

    def create(self, **kwargs):
        api_key = os.getenv("HUGGINGFACE_HUB_ACCESS_TOKEN")
        model = kwargs.get("model", default_model)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        temperature = kwargs.get("temperature", 0.7)
        params = {}

        if api_key:
            params["api_token"] = api_key
        if model:
            params["model"] = model
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts

        try:
            driver = HuggingFaceHubPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
