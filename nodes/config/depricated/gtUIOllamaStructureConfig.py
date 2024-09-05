from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    OllamaPromptDriver,
)

from ..gtUIBaseConfig import gtUIBaseConfig

ollama_port = "11434"
ollama_base_url = "http://127.0.0.1"


class gtUIOllamaStructureConfig(gtUIBaseConfig):
    """
    The Griptape Ollama Structure Config
    """

    DESCRIPTION = "Ollama Prompt Driver. Use local models with Ollama. Available at https://ollama.com"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": ((), {}),
                "base_url": ("STRING", {"default": ollama_base_url}),
                "port": ("STRING", {"default": ollama_port}),
            },
        )
        return inputs

    def create(self, **kwargs):
        params = {}

        params["model"] = kwargs.get("prompt_model", "")
        params["temperature"] = kwargs.get("temperature", 0.7)
        port = kwargs.get("port", ollama_port)
        base_url = kwargs.get("base_url", ollama_base_url)
        params["host"] = f"{base_url}:{port}"
        params["stream"] = kwargs.get("stream", False)
        params["use_native_tools"] = kwargs.get("use_native_tools", False)
        params["max_attempts"] = kwargs.get("max_attempts_on_fail", 10)
        max_tokens = kwargs.get("max_tokens", -1)
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        custom_config = DriversConfig(
            prompt_driver=OllamaPromptDriver(**params),
        )

        return (custom_config,)
