from griptape.drivers.prompt.ollama import OllamaPromptDriver
from rich import print

from ...py.griptape_settings import GriptapeSettings
from .gtUIBasePromptDriver import gtUIBasePromptDriver

default_port = "11434"
default_base_url = "http://127.0.0.1"


class gtUIOllamaPromptDriver(gtUIBasePromptDriver):
    @classmethod
    def get_default_url(cls):
        settings = GriptapeSettings()
        # settings.read_settings()
        default_url = settings.get_settings_key_or_use_env("ollama_base_url")
        if not default_url or default_url == "":
            default_url = default_base_url
        return default_url

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
        inputs["required"].update(
            {
                "base_url": (
                    "STRING",
                    {
                        "default": cls.get_default_url(),
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
        # inputs["optional"]["model"] = ((), {"tooltip": "The prompt model to use"})
        inputs["optional"]["model"] = (
            "STRING",
            {"tooltip": "The prompt model to use"},
        )
        inputs["optional"]["keep_alive"] = (
            "INT",
            {
                "default": 240,
                "tooltip": "Seconds to keep the connection alive",
            },
        )
        return inputs

    FUNCTION = "create"

    @classmethod
    def VALIDATE_INPUTS(cls, keep_alive, **kwargs):
        if keep_alive < 0:
            return "Keep alive must be greater than or equal to 0"
        return True

    def build_params(self, **kwargs):
        model = kwargs.get("model", None)
        base_url = kwargs.get("base_url", self.get_default_url())
        port = kwargs.get("port", default_port)
        temperature = kwargs.get("temperature", None)
        max_attempts = kwargs.get("max_attempts_on_fail", None)
        use_native_tools = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", None)
        keep_alive = kwargs.get("keep_alive", 240)
        min_p = kwargs.get("min_p")
        top_k = kwargs.get("top_k")
        params = {
            "model": model,
            "temperature": temperature,
            "max_attempts": max_attempts,
            "use_native_tools": use_native_tools,
        }
        if base_url and port:
            params["host"] = f"{base_url}:{port}"
        if max_tokens > 0:
            params["max_tokens"] = max_tokens
        params["extra_params"] = {
            "keep_alive": int(keep_alive),
            "options": {
                "min_p": min_p,
                "top_k": top_k,
            },
        }
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        try:
            driver = OllamaPromptDriver(**params)
            return (driver,)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return (None, str(e))
