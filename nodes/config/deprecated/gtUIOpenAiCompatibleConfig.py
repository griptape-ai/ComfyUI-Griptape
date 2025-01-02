from dotenv import load_dotenv
from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    OpenAiChatPromptDriver,
    OpenAiImageGenerationDriver,
    OpenAiTextToSpeechDriver,
)

from ..gtUIBaseConfig import gtUIBaseConfig

load_dotenv()

DEFAULT_API_KEY = "OPENAI_API_KEY"


class gtUIOpenAiCompatibleConfig(gtUIBaseConfig):
    """
    Create an OpenAI Compatible Structure Config
    """

    DESCRIPTION = "OpenAI Compatible Structure Config."

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "prompt_model": ("STRING", {"default": "gpt-4o"}),
                "image_generation_model": ("STRING", {"default": "dall-e-3"}),
                "text_to_speech_model": ("STRING", {"default": "tts-1"}),
                "base_url": ("STRING", {"default": "https://api.openai.com/v1"}),
                "api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY},
                ),
            }
        )
        return inputs

    def create(self, **kwargs):
        params = {}

        params["model"] = kwargs.get("prompt_model", None)
        params["base_url"] = kwargs.get("base_url", None)
        params["max_attempts"] = kwargs.get("max_attempts_on_fail", 2)
        params["stream"] = kwargs.get("stream", False)
        params["use_native_tools"] = kwargs.get("use_native_tools", False)
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_API_KEY)
        params["api_key"] = self.getenv(api_key_env_var)
        image_generation_model = kwargs.get("image_generation_model", None)
        text_to_speech_model = kwargs.get("text_to_speech_model", None)
        max_tokens = kwargs.get("max_tokens", -1)
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        if not params["api_key"]:
            params["api_key"] = api_key_env_var
        configs = {}
        if params["model"] and params["base_url"] and params["api_key"]:
            configs["prompt_driver"] = OpenAiChatPromptDriver(**params)
        if image_generation_model and params["base_url"] and params["api_key"]:
            configs["image_generation_driver"] = OpenAiImageGenerationDriver(
                model=image_generation_model,
                base_url=params["base_url"],
                api_key=params["api_key"],
            )

        if text_to_speech_model and params["base_url"] and params["api_key"]:
            configs["text_to_speech_driver"] = OpenAiTextToSpeechDriver(
                model=text_to_speech_model,
                base_url=params["base_url"],
                api_key=params["api_key"],
            )
        custom_config = DriversConfig(**configs)
        return (custom_config,)
