import os

from griptape.drivers import CoherePromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = [
    "command-r-plus",
    "command-r",
    "command",
    "command-light",
    "command-nightly",
    "command-light-nightly",
]


class gtUICoherePromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
            }
        )
        inputs["optional"].update({})

        del inputs["optional"]["temperature"]
        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Drivers/Prompt"

    def create(self, **kwargs):
        api_key = os.getenv("COHERE_API_KEY")
        model = kwargs.get("model", models[0])
        stream = kwargs.get("stream", False)
        max_attempts = kwargs.get("max_attempts_on_fail", None)

        params = {}

        if api_key:
            params["api_key"] = api_key
        if model:
            params["model"] = model
        if stream:
            params["stream"] = stream
        if max_attempts:
            params["max_attempts"] = max_attempts

        try:
            driver = CoherePromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
