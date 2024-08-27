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

from .gtUIBaseConfig import gtUIBaseConfig

load_dotenv()

DEFAULT_API_KEY = "OPENAI_API_KEY"


class gtUIOpenAiCompatibleConfig(gtUIBaseConfig):
    """
    Create an OpenAI Compatible Structure Config
    """

    DESCRIPTION = "OpenAI Compatible Structure Config."

    @classmethod
    def INPUT_TYPES(s):
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
                "use_native_tools": ("BOOLEAN", {"default": False}),
            }
        )
        return inputs

    def create(self, **kwargs):
        prompt_model = kwargs.get("prompt_model", None)
        image_generation_model = kwargs.get("image_generation_model", None)
        text_to_speech_model = kwargs.get("text_to_speech_model", None)
        base_url = kwargs.get("base_url", None)
        max_attempts = kwargs.get("max_attempts_on_fail", 10)
        stream = kwargs.get("stream", False)
        use_native_tools = kwargs.get("use_native_tools", False)
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_API_KEY)
        api_key = self.getenv(api_key_env_var)
        if not api_key:
            api_key = api_key_env_var
        configs = {}
        if prompt_model and base_url and api_key:
            configs["prompt_driver"] = OpenAiChatPromptDriver(
                model=prompt_model,
                base_url=base_url,
                api_key=api_key,
                max_attempts=max_attempts,
                stream=stream,
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
        if use_native_tools:
            configs["use_native_tools"] = use_native_tools
        custom_config = DriversConfig(**configs)
        return (custom_config,)
