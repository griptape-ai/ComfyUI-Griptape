from griptape.drivers import OpenAiChatPromptDriver

from .gtUIOpenAiCompatibleChatPromptDriver import gtUIOpenAiCompatibleChatPromptDriver

default_port = "1234"
default_base_url = "http://127.0.0.1"
DEFAULT_API_KEY = "lm_studio"


class gtUILMStudioChatPromptDriver(gtUIOpenAiCompatibleChatPromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        del inputs["optional"]["api_key_env_var"]

        inputs["optional"].update(
            {
                "model": ((), {"tooltip": "The model to use for the chat prompt."}),
                "base_url": (
                    "STRING",
                    {
                        "default": default_base_url,
                        "tooltip": "The base URL for the API.",
                    },
                ),
                "port": (
                    "STRING",
                    {
                        "default": default_port,
                        "tooltip": "The port to connect to the API.",
                    },
                ),
                "use_native_tools": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "Whether to use native tools."},
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY,
                        "tooltip": "API key for authentication.",
                    },
                ),
            }
        )

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("model", None)
        base_url = kwargs.get("base_url", default_base_url)
        port = kwargs.get("port")
        response_format = kwargs.get("response_format", None)
        api_key = kwargs.get("api_key")
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)

        params = {
            "model": model,
            "base_url": f"{base_url}:{port}/v1",
            "api_key": api_key,
            "temperature": temperature,
            "use_native_tools": use_native_tools,
            "max_attempts": max_attempts,
        }
        if response_format == "json_object":
            params["response_format"] = {"type": response_format}
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
