import os

from griptape.drivers import OpenAiChatPromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = ["gpt-4o", "gpt-4", "gpt-4o-mini", "gpt-3.5-turbo"]


class gtUIOpenAiChatPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
                "response_format": (["default", "json_object"], {"default": "default"}),
            }
        )
        inputs["optional"].update({})

        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Drivers/Prompt"

    def create(self, **kwargs):
        api_key = os.getenv("OPENAI_API_KEY")
        model = kwargs.get("model", None)
        response_format = kwargs.get("response_format", None)
        seed = kwargs.get("seed", None)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)

        params = {}

        if api_key:
            params["api_key"] = api_key
        if model:
            params["model"] = model
        if not response_format == "default":
            params["response_format"] = response_format
        if seed:
            params["seed"] = seed
        if stream:
            params["stream"] = stream
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts

        try:
            driver = OpenAiChatPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
