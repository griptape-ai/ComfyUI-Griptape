# pyright: reportMissingImports=false
from comfy_execution.graph import ExecutionBlocker
from griptape.drivers.prompt.openai import OpenAiChatPromptDriver

from .gtUIOpenAiCompatibleChatPromptDriver import gtUIOpenAiCompatibleChatPromptDriver

default_port = "1234"
default_base_url = "http://127.0.0.1"
DEFAULT_API_KEY = "lm_studio"


class gtUILMStudioChatPromptDriver(gtUIOpenAiCompatibleChatPromptDriver):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        del inputs["optional"]["api_key_env_var"]

        inputs["optional"].update(
            {
                "model": (
                    "STRING",
                    {"tooltip": "The model to use for the chat prompt."},
                ),
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
                    {
                        "default": False,
                        "tooltip": "Whether to use native tools.",
                        "label_on": "True (LLM-native tool calling)",
                        "label_off": "False (Griptape tool calling)",
                    },
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
        top_p = 1 - kwargs.get("min_p", None)
        params = {
            "model": model,
            "base_url": f"{base_url}:{port}/v1",
            "api_key": api_key,
            "temperature": temperature,
            "use_native_tools": use_native_tools,
            "max_attempts": max_attempts,
            "extra_params": {
                "top_p": top_p,
                # "top_k": top_k,
            },
        }
        if response_format == "json_object":
            params["response_format"] = {"type": response_format}
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        if not params.get("model"):
            driver = ExecutionBlocker("Model is required.")
            return (driver,)
        try:
            driver = OpenAiChatPromptDriver(**params)
            return (driver,)
        except Exception as e:
            driver = ExecutionBlocker(f"Error creating driver: {e}")
            return (driver,)
