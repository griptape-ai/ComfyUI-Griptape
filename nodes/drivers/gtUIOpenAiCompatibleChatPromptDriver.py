from griptape.drivers import OpenAiChatPromptDriver

from .gtUIOpenAiChatPromptDriver import gtUIOpenAiChatPromptDriver

default_model = "gpt-4o"
default_base_url = "https://api.openai.com/v1"
DEFAULT_API_KEY_ENV = "OPENAI_API_KEY"


class gtUIOpenAiCompatibleChatPromptDriver(gtUIOpenAiChatPromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "model": (
                    "STRING",
                    {
                        "default": default_model,
                        "tooltip": "The model to use, e.g., gpt-4o",
                    },
                ),
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

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("model", None)
        base_url = kwargs.get("base_url", default_base_url)
        response_format = kwargs.get("response_format", None)
        if kwargs.get("api_key"):
            api_key = kwargs.get("api_key")
        else:
            api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV))
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)

        params = {
            "model": model,
            "base_url": base_url,
            "api_key": api_key,
            "temperature": temperature,
            "use_native_tools": use_native_tools,
            "max_attempts": max_attempts,
        }
        if response_format == "json_object":
            response_format = {"type": "json_object"}
            params["response_format"] = response_format
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        try:
            driver = OpenAiChatPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
