from dotenv import load_dotenv
from griptape.config import (
    StructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    OpenAiChatPromptDriver,
    OpenAiImageGenerationDriver,
    OpenAiTextToSpeechDriver,
)

from .gtUIBaseConfig import gtUIBaseConfig

load_dotenv()

default_api_key = "OPENAI_API_KEY"


class gtUIOpenAiCompatableConfig(gtUIBaseConfig):
    """
    Create an OpenAI Compatable Structure Config
    """

    DESCRIPTION = "OpenAI Compatable Structure Config."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "prompt_model": ("STRING", {"default": "gpt-4o"}),
                "image_generation_model": ("STRING", {"default": "dall-e-3"}),
                "text_to_speech_model": ("STRING", {"default": "tts-1"}),
                "prompt_base_url": ("STRING", {"default": "https://api.openai.com/v1"}),
                "api_key_env_var": (
                    "STRING",
                    {"default": default_api_key},
                ),
            }
        )
        return inputs

    def create(self, **kwargs):
        prompt_model = kwargs.get("prompt_model", None)
        image_generation_model = kwargs.get("image_generation_model", None)
        text_to_speech_model = kwargs.get("text_to_speech_model", None)
        base_url = kwargs.get("prompt_base_url", None)
        max_attempts = kwargs.get("max_attempts_on_fail", 10)

        api_key = self.getenv(kwargs.get("api_key_env_var", default_api_key))

        configs = {}
        if prompt_model and base_url and api_key:
            configs["prompt_driver"] = OpenAiChatPromptDriver(
                model=prompt_model,
                base_url=base_url,
                api_key=api_key,
                max_attempts=max_attempts,
            )
        if image_generation_model and base_url and api_key:
            configs["image_generation_driver"] = OpenAiImageGenerationDriver(
                model=image_generation_model,
                base_url=base_url,
                api_key=api_key,
            )

        if text_to_speech_model and base_url and api_key:
            configs["text_to_speech_driver"] = OpenAiTextToSpeechDriver(
                model=text_to_speech_model,
                base_url=base_url,
                api_key=api_key,
            )
        custom_config = StructureConfig(**configs)

        return (custom_config,)
