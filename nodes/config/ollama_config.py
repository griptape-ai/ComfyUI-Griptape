from griptape.config import (
    StructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    DummyImageGenerationDriver,
    OllamaPromptDriver,
)

from ..utilities import get_ollama_models
from .base_config import gtUIBaseConfig

ollama_models = get_ollama_models()
ollama_models.append("")
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
                "prompt_model": (
                    [""],
                    {"default": ""},
                ),
                "base_url": ("STRING", {"default": ollama_base_url}),
                "port": ("STRING", {"default": ollama_port}),
            },
        )
        return inputs

    def create(self, **kwargs):
        prompt_model = kwargs.get("prompt_model", "")
        temperature = kwargs.get("temperature", 0.7)
        base_url = kwargs.get("base_url", ollama_base_url)
        port = kwargs.get("port", ollama_port)
        seed = kwargs.get("seed", 12341)

        image_generation_driver = kwargs.get(
            "image_generation_driver", DummyImageGenerationDriver()
        )
        max_attempts = kwargs.get("max_attempts_on_fail", 10)

        custom_config = StructureConfig(
            prompt_driver=OllamaPromptDriver(
                model=prompt_model,
                temperature=temperature,
                host=f"{base_url}:{port}",
                max_attempts=max_attempts,
            ),
            image_generation_driver=image_generation_driver,
        )

        return (custom_config,)
