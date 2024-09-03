from griptape.drivers import OllamaPromptDriver

from .gtUIBasePromptDriver import gtUIBasePromptDriver

default_port = "11434"
default_base_url = "http://127.0.0.1"


class gtUIOllamaPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        # Get the base required and optional inputs
        base_required_inputs = inputs["required"]
        base_optional_inputs = inputs["optional"]

        # Clear the required and optional inputs
        inputs["required"] = {}
        inputs["optional"] = {}

        # Add the base required inputs to the inputs
        inputs["required"].update(
            {
                "base_url": (
                    "STRING",
                    {
                        "default": default_base_url,
                        "tooltip": "The base URL of the Ollama server",
                    },
                ),
                "port": (
                    "STRING",
                    {
                        "default": default_port,
                        "tooltip": "The port of the Ollama server",
                    },
                ),
            }
        )

        # Add the base required inputs to the inputs
        inputs["required"].update(base_required_inputs)

        # Add the base optional inputs to the inputs
        inputs["optional"].update(base_optional_inputs)

        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        model = kwargs.get("model", None)
        base_url = kwargs.get("base_url", default_base_url)
        port = kwargs.get("port", default_port)
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)

        params = {}

        if model:
            params["model"] = model
        if stream:
            params["stream"] = stream
        if temperature:
            params["temperature"] = temperature
        if max_attempts:
            params["max_attempts"] = max_attempts
        if base_url and port:
            params["host"] = f"{base_url}:{port}"
        if use_native_tools:
            params["use_native_tools"] = use_native_tools
        if max_tokens > 0:
            params["max_tokens"] = max_tokens
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        try:
            driver = OllamaPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
