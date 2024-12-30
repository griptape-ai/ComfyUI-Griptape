from griptape.configs import Defaults
from griptape.configs.drivers import (
    OpenAiDriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    OpenAiChatPromptDriver,
)

from ..gtUIBaseConfig import gtUIBaseConfig

default_prompt_model = "gpt-4o"
default_image_query_model = "gpt-4o"
DEFAULT_API_KEY = "OPENAI_API_KEY"


class gtUIOpenAiStructureConfig(gtUIBaseConfig):
    """
    The Griptape OpenAI Structure Config
    """

    DESCRIPTION = "OpenAI Structure Config. Use OpenAI's models for prompt, embedding, image generation, and image query."

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    ["gpt-4o", "gpt-4", "gpt-4o-mini", "gpt-3.5-turbo"],
                    {"default": default_prompt_model},
                ),
            }
        )
        inputs["optional"].update(
            {
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY}),
            }
        )
        return inputs

    def create(
        self,
        **kwargs,
    ):
        params = {}
        params["model"] = kwargs.get("prompt_model", default_prompt_model)
        params["temperature"] = kwargs.get("temperature", 0.7)
        params["seed"] = kwargs.get("seed", 12341)
        params["max_attempts"] = kwargs.get("max_attempts_on_fail", 10)
        params["api_key"] = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))
        params["use_native_tools"] = kwargs.get("use_native_tools", False)
        max_tokens = kwargs.get("max_tokens", -1)
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        try:
            Defaults.drivers_config = OpenAiDriversConfig(
                prompt_driver=OpenAiChatPromptDriver(**params)
            )

            # OpenAiStructureConfig()
            custom_config = Defaults.drivers_config
        except Exception as e:
            raise Exception(f"Error creating OpenAiStructureConfig: {e}")

        return (custom_config,)
