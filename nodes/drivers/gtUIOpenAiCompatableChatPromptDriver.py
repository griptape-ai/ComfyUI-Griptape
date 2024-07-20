from griptape.drivers import OpenAiChatPromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

default_model = "gpt-4o"
default_base_url = "https://api.openai.com/v1"
DEFAULT_API_KEY_ENV = "OPENAI_API_KEY"


class gtUIOpenAiCompatableChatPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["required"].update(
            {
                "model": ("STRING", {"default": default_model}),
                "base_url": ("STRING", {"default": default_base_url}),
            }
        )
        inputs["optional"].update(
            {
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY_ENV}),
            }
        )

        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Drivers/Prompt"

    def create(self, **kwargs):
        model = kwargs.get("model", None)
        base_url = kwargs.get("base_url", default_base_url)
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)

        params = {}

        if model:
            params["model"] = model
        if stream:
            params["stream"] = stream
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts
        if base_url:
            params["base_url"] = base_url
        if api_key_env_var:
            params["api_key"] = self.getenv(api_key_env_var)

        try:
            driver = OpenAiChatPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
