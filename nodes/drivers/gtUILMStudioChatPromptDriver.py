from griptape.drivers import OpenAiChatPromptDriver

from ..utilities import get_lmstudio_models
from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = get_lmstudio_models()
models.append("")
default_port = "1234"
default_base_url = "http://127.0.0.1"
DEFAULT_API_KEY = "lm_studio"


class gtUILMStudioChatPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": ([], {"default": ""}),
                "base_url": ("STRING", {"default": default_base_url}),
                "port": ("STRING", {"default": default_port}),
            }
        )
        inputs["optional"].update({})

        return inputs

    FUNCTION = "create"

    def create(self, **kwargs):
        model = kwargs.get("model", None)
        base_url = kwargs.get("base_url", default_base_url)
        port = kwargs.get("port", default_port)
        api_key = DEFAULT_API_KEY
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)

        params = {}

        if model:
            params["model"] = model
        if api_key:
            params["api_key"] = api_key
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts
        if base_url:
            params["base_url"] = f"{base_url}:{port}/v1"

        try:
            driver = OpenAiChatPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
