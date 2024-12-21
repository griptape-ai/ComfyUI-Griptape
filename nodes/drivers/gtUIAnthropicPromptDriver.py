from griptape.drivers import AnthropicPromptDriver

from ..utils.anthropic_utils import get_available_models
from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = get_available_models("ModelParam")

DEFAULT_MODEL = "claude-3-5-sonnet-latest"
DEFAULT_API_KEY = "ANTHROPIC_API_KEY"


class gtUIAnthropicPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        # Get the base required and optional inputs
        base_required_inputs = inputs["required"]
        base_optional_inputs = inputs["optional"]

        # Add the base required inputs to the inputs
        inputs["required"].update(base_required_inputs)

        # Add the optional inputs
        inputs["optional"].update(base_optional_inputs)

        # Set model default
        inputs["optional"]["model"] = (
            models,
            {
                "default": DEFAULT_MODEL,
                "tooltip": "Select the model you want to use from the available options.",
            },
        )
        inputs["optional"].update(
            {
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY,
                        "tooltip": "Enter the name of the environment variable for your ANTHROPIC_API_KEY key, not your actual key.",
                    },
                ),
                "top_p": (
                    "FLOAT",
                    {
                        "default": 0.999,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.01,
                        "tooltip": "Controls the cumulative probability distribution cutoff. The model will only consider the top p% most probable tokens.",
                    },
                ),
                "top_k": (
                    "INT",
                    {
                        "default": 250,
                        "min": 0,
                        "max": 500,
                        "step": 1,
                        "tooltip": "Limits the number of tokens considered for each step of the generation. Pevents the model from focusing too narrowly on the top choices.",
                    },
                ),
            }
        )

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("model", DEFAULT_MODEL)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)
        top_p = kwargs.get("top_p", None)
        top_k = kwargs.get("top_k", None)
        params = {
            "api_key": api_key,
            "model": model,
            "stream": stream,
            "temperature": temperature,
            "max_attempts": max_attempts,
            "use_native_tools": use_native_tools,
        }
        if max_tokens > 0:
            params["max_tokens"] = max_tokens
        if top_p:
            params["top_p"] = top_p
        if top_k:
            params["top_k"] = top_k

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        try:
            driver = AnthropicPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
