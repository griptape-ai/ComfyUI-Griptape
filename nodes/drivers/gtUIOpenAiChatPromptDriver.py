from griptape.drivers import OpenAiChatPromptDriver

from ..utils.openai_utils import get_available_models
from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = get_available_models("ChatModel")

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_API_KEY = "OPENAI_API_KEY"


class gtUIOpenAiChatPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        # Get the base required and optional inputs
        base_required_inputs = inputs["required"]
        base_optional_inputs = inputs["optional"]

        # Clear the required and optional inputs
        inputs["required"] = {}
        inputs["optional"] = {}

        # Add the base required inputs to the inputs
        inputs["required"].update(base_required_inputs)

        # Add the optional inputs
        inputs["optional"].update(base_optional_inputs)

        # Set model default
        inputs["optional"]["model"] = (models, {"default": DEFAULT_MODEL})
        inputs["optional"].update(
            {
                "response_format": (
                    ["default", "json_object"],
                    {"default": "default", "tooltip": "Format of the response"},
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY,
                        "tooltip": "Enter the environment variable name, not the actual API key",
                    },
                ),
            }
        )

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))
        model = kwargs.get("model", DEFAULT_MODEL)
        response_format = kwargs.get("response_format", None)
        seed = kwargs.get("seed", None)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)
        params = {}

        if api_key:
            params["api_key"] = api_key
        if model:
            params["model"] = model
        if response_format == "json_object":
            response_format = {"type": "json_object"}
            params["response_format"] = response_format
        if seed:
            params["seed"] = seed
        if stream:
            params["stream"] = stream
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts
        if use_native_tools:
            params["use_native_tools"] = use_native_tools
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
