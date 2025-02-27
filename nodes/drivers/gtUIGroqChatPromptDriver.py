# pyright: reportMissingImports=false
from comfy_execution.graph import ExecutionBlocker
from griptape.drivers.prompt.openai import OpenAiChatPromptDriver

from .gtUIOpenAiCompatibleChatPromptDriver import gtUIOpenAiCompatibleChatPromptDriver

default_base_url = "https://api.groq.com/openai/v1"
DEFAULT_API_KEY_ENV = "GROQ_API_KEY"
models = [
    "gemma2-9b-it",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-guard-3-8b",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "llama-3.3-70b-specdec",
    "llama-3.2-1b-preview",
    "llama-3.2-3b-preview",
    "llama-3.2-11b-vision-preview",
    "llama-3.2-90b-vision-preview",
]


class gtUIGroqChatPromptDriver(gtUIOpenAiCompatibleChatPromptDriver):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        del inputs["optional"]["base_url"]
        inputs["optional"].update(
            {
                "model": (
                    models,
                    {
                        "default": models[0],
                        "tooltip": "The model to use for the chat prompt.",
                    },
                ),
                "use_native_tools": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "Whether to use native tools.",
                        "label_on": "True (LLM-native tool calling)",
                        "label_off": "False (Griptape tool calling)",
                    },
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV,
                        "tooltip": "API key variable for authentication.",
                    },
                ),
            }
        )

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("model", None)
        response_format = kwargs.get("response_format", None)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV))

        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)

        params = {
            "model": model,
            "base_url": default_base_url,
            "api_key": api_key,
            "temperature": temperature,
            "use_native_tools": use_native_tools,
            "max_attempts": max_attempts,
            "modalities": [],
            "extra_params": {
                "top_p": 1 - kwargs.get("min_p", None),
            },
        }
        if response_format == "json_object":
            params["response_format"] = {"type": response_format}
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        print(params)
        if not params.get("model"):
            driver = ExecutionBlocker("Model is required.")
            return (driver,)
        try:
            driver = OpenAiChatPromptDriver(**params)
            return (driver,)
        except Exception as e:
            driver = ExecutionBlocker(f"Error creating driver: {e}")
            return (driver,)
