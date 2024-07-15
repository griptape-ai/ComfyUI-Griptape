from griptape.config import (
    OpenAiStructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    OpenAiChatPromptDriver,
    OpenAiEmbeddingDriver,
    OpenAiImageGenerationDriver,
    OpenAiImageQueryDriver,
)

from ...py.griptape_config import get_config
from .base_config import gtUIBaseConfig

default_prompt_model = "gpt-4o"
default_image_query_model = "gpt-4o"


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
                    ["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
                    {"default": default_prompt_model},
                ),
                "image_query_model": (
                    ["gpt-4o", "gpt-4-vision-preview"],
                    {"default": default_image_query_model},
                ),
            }
        )
        return inputs

    def create(
        self,
        **kwargs,
    ):
        prompt_model = kwargs.get("prompt_model", default_prompt_model)
        image_query_model = kwargs.get("image_query_model", default_image_query_model)
        temperature = kwargs.get("temperature", 0.7)
        seed = kwargs.get("seed", 12341)
        image_generation_driver = kwargs.get("image_generation_driver", None)
        max_attempts = kwargs.get("max_attempts_on_fail", 10)

        OPENAI_API_KEY = get_config("env.OPENAI_API_KEY")
        prompt_driver = OpenAiChatPromptDriver(
            model=prompt_model,
            api_key=OPENAI_API_KEY,
            temperature=temperature,
            seed=seed,
            max_attempts=max_attempts,
        )
        embedding_driver = OpenAiEmbeddingDriver(api_key=OPENAI_API_KEY)
        if not image_generation_driver:
            image_generation_driver = OpenAiImageGenerationDriver(
                api_key=OPENAI_API_KEY,
                model="dall-e-3",
            )

        image_query_driver = OpenAiImageQueryDriver(
            api_key=OPENAI_API_KEY, model=image_query_model
        )

        # OpenAiStructureConfig()
        custom_config = OpenAiStructureConfig(
            prompt_driver=prompt_driver,
            embedding_driver=embedding_driver,
            image_generation_driver=image_generation_driver,
            image_query_driver=image_query_driver,
        )

        return (custom_config,)
