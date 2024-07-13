from griptape.config import (
    AnthropicStructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AnthropicImageQueryDriver,
    AnthropicPromptDriver,
    DummyImageGenerationDriver,
)

from .base_config import gtUIBaseConfig

anthropicPromptModels = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]
anthropicImageQueryModels = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]
voyageAiEmbeddingModels = [
    "voyage-large-2",
]


class gtUIAnthropicStructureConfig(gtUIBaseConfig):
    """
    The Griptape Anthropic Structure Config
    """

    DESCRIPTION = (
        "Anthropic Structure Config. Use Anthropic's models for prompt and image query."
    )

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    anthropicPromptModels,
                    {"default": anthropicPromptModels[0]},
                ),
                "image_query_model": (
                    anthropicImageQueryModels,
                    {"default": anthropicImageQueryModels[0]},
                ),
            },
        )
        return inputs

    def create(
        self,
        prompt_model,
        image_query_model,
        temperature,
        seed,
        image_generation_driver=DummyImageGenerationDriver(),
    ):
        custom_config = AnthropicStructureConfig()
        custom_config.prompt_driver = AnthropicPromptDriver(
            model=prompt_model, temperature=temperature
        )
        custom_config.image_query_driver = AnthropicImageQueryDriver(
            model=image_query_model
        )
        custom_config.image_generation_driver = image_generation_driver

        return (custom_config,)
