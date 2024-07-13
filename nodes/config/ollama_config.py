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

    def create(
        self,
        prompt_model,
        temperature,
        base_url,
        port,
        seed,
        image_generation_driver=DummyImageGenerationDriver(),
    ):
        custom_config = StructureConfig(
            prompt_driver=OllamaPromptDriver(
                model=prompt_model,
                options={"temperature": temperature},
                host=f"{base_url}:{port}",
            ),
            image_generation_driver=image_generation_driver,
        )

        return (custom_config,)
