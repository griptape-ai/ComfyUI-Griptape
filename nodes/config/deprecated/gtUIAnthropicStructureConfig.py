from griptape.configs.drivers import (
    AnthropicDriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AnthropicPromptDriver,
)

from ..gtUIBaseConfig import gtUIBaseConfig

anthropicPromptModels = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

DEFAULT_API_KEY = "ANTHROPIC_API_KEY"


class gtUIAnthropicStructureConfig(gtUIBaseConfig):
    """
    The Griptape Anthropic Structure Config
    """

    DESCRIPTION = (
        "Anthropic Structure Config. Use Anthropic's models for prompt and image query."
    )

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    anthropicPromptModels,
                    {"default": anthropicPromptModels[0]},
                ),
            },
        )
        inputs["optional"].update(
            {
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY}),
            },
        )
        return inputs

    def create(
        self,
        **kwargs,
    ):
        params = {}

        params["model"] = kwargs.get("prompt_model", anthropicPromptModels[0])
        params["temperature"] = kwargs.get("temperature", 0.7)
        params["max_attempts"] = kwargs.get("max_attempts_on_fail", 2)
        params["use_native_tools"] = kwargs.get("use_native_tools", True)
        params["api_key"] = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))

        max_tokens = kwargs.get("max_tokens", None)
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        custom_config = AnthropicDriversConfig(
            prompt_driver=AnthropicPromptDriver(**params)
        )

        return (custom_config,)
