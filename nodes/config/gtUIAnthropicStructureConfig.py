from griptape.config import (
    AnthropicStructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AnthropicImageQueryDriver,
    AnthropicPromptDriver,
    DummyImageGenerationDriver,
)

from .gtUIBaseConfig import gtUIBaseConfig

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
        **kwargs,
    ):
        prompt_model = kwargs.get("prompt_model", anthropicPromptModels[0])
        image_query_model = kwargs.get(
            "image_query_model", anthropicImageQueryModels[0]
        )
        temperature = kwargs.get("temperature", 0.7)
        image_generation_driver = kwargs.get(
            "image_generation_driver", DummyImageGenerationDriver()
        )
        max_attempts = kwargs.get("max_attempts_on_fail", 10)

        custom_config = AnthropicStructureConfig()
        custom_config.prompt_driver = AnthropicPromptDriver(
            model=prompt_model, temperature=temperature, max_attempts=max_attempts
        )
        custom_config.image_query_driver = AnthropicImageQueryDriver(
            model=image_query_model
        )
        custom_config.image_generation_driver = image_generation_driver

        return (custom_config,)
