from griptape.configs.drivers import (
    OpenAiDriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    OpenAiChatPromptDriver,
)

from .gtUIBaseConfig import gtUIBaseConfig

default_prompt_model = "gpt-4o"
default_image_query_model = "gpt-4o"
DEFAULT_API_KEY = "OPENAI_API_KEY"


class gtUIOpenAiStructureConfig(gtUIBaseConfig):
    """
    The Griptape OpenAI Structure Config
    """

    DESCRIPTION = "OpenAI Structure Config. Use OpenAI's models for prompt, embedding, image generation, and image query."

    @classmethod
    def INPUT_TYPES(s):
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
        prompt_model = kwargs.get("prompt_model", default_prompt_model)
        temperature = kwargs.get("temperature", 0.7)
        seed = kwargs.get("seed", 12341)
        max_attempts = kwargs.get("max_attempts_on_fail", 10)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))

        try:
            prompt_driver = OpenAiChatPromptDriver(
                model=prompt_model,
                api_key=api_key,
                temperature=temperature,
                seed=seed,
                max_attempts=max_attempts,
            )

            # OpenAiStructureConfig()
            custom_config = OpenAiDriversConfig(
                prompt_driver=prompt_driver,
            )
        except Exception as e:
            raise Exception(f"Error creating OpenAiStructureConfig: {e}")

        return (custom_config,)
