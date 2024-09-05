from griptape.drivers import AnthropicPromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

models = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

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
        inputs["optional"]["model"] = (models, {"default": models[0]})
        inputs["optional"].update(
            {
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY}),
            }
        )

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("model", None)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)
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

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        try:
            driver = AnthropicPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
