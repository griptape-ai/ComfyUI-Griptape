from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    DummyEmbeddingDriver,
    OllamaEmbeddingDriver,
    OllamaPromptDriver,
)

from .gtUIBaseConfig import gtUIBaseConfig

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
        optional_inputs = inputs["optional"]
        # Clear optional inputs
        # env always has to be set first

        env_input = optional_inputs.pop("env")
        inputs["optional"] = {"env": env_input}

        inputs["optional"].update(
            {
                "ollama_settings_comment": (
                    "STRING",
                    {
                        "default": "Ollama Settings",
                    },
                ),
                "base_url": ("STRING", {"default": ollama_base_url}),
                "port": ("STRING", {"default": ollama_port}),
                "prompt_model_comment": (
                    "STRING",
                    {
                        "default": "Prompt Model",
                    },
                ),
                "prompt_model": ((), {}),
            }
        )
        # add optional inputs as required
        inputs["optional"].update(optional_inputs)

        # Now add the embedding model
        inputs["optional"].update(
            {
                "embedding_model_comment": (
                    "STRING",
                    {
                        "default": "Embedding Model",
                    },
                ),
                "embedding_model": ((), {}),
            },
        )

        return inputs

    def create(self, **kwargs):
        drivers_config_params = {}

        prompt_driver_params = {}
        embedding_driver_params = {}

        prompt_driver_params["model"] = kwargs.get("prompt_model", "")
        prompt_driver_params["temperature"] = kwargs.get("temperature", 0.7)
        port = kwargs.get("port", ollama_port)
        base_url = kwargs.get("base_url", ollama_base_url)
        prompt_driver_params["host"] = f"{base_url}:{port}"
        embedding_driver_params["host"] = f"{base_url}:{port}"

        prompt_driver_params["stream"] = kwargs.get("stream", False)
        prompt_driver_params["use_native_tools"] = kwargs.get("use_native_tools", False)
        prompt_driver_params["max_attempts"] = kwargs.get("max_attempts_on_fail", 10)
        embedding_driver_params["max_attempts"] = kwargs.get("max_attempts_on_fail", 10)
        max_tokens = kwargs.get("max_tokens", -1)
        if max_tokens > 0:
            prompt_driver_params["max_tokens"] = max_tokens

        prompt_driver = OllamaPromptDriver(**prompt_driver_params)

        embedding_driver_model = kwargs.get("embedding_model", None)
        if embedding_driver_model:
            embedding_driver_params["model"] = embedding_driver_model
            embedding_driver = OllamaEmbeddingDriver(**embedding_driver_params)
        else:
            embedding_driver = DummyEmbeddingDriver()

        drivers_config_params["prompt_driver"] = prompt_driver
        drivers_config_params["embedding_driver"] = embedding_driver
        custom_config = DriversConfig(**drivers_config_params)

        return (custom_config,)
