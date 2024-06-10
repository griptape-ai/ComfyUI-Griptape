import os

from griptape.config import (
    AmazonBedrockStructureConfig,
    AnthropicStructureConfig,
    GoogleStructureConfig,
    StructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AnthropicImageQueryDriver,
    OpenAiChatPromptDriver,
    OpenAiEmbeddingDriver,
    OpenAiImageGenerationDriver,
    OpenAiImageQueryDriver,
)

from ..py.griptape_config import get_config
from .base_config import gtUIBaseConfig


class gtUIEnv:
    """
    The Griptape Environment Config
    Setting environment variables
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "Environment Vars": ("STRING", {"default": "ENV=", "multiline": True})
            },
        }

    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ENVIRS",)
    OUTPUT_NODE = True

    CATEGORY = "Griptape"

    def run(self, **kwargs):
        envirs = kwargs.get("Environment Vars", "")
        environment_vars = []
        for envir in envirs.split("\n"):
            if "=" in envir:
                key, value = envir.split("=", 1)
                if key and value:
                    os.environ[key] = value
                    environment_vars.append(f"{key}={value}")
        return (environment_vars,)


class gtUIAmazonBedrockStructureConfig(gtUIBaseConfig):
    """
    The Griptape Amazon Bedrock Structure Config
    """

    def create(
        self,
    ):
        custom_config = AmazonBedrockStructureConfig()

        return (custom_config,)


class gtUIGoogleStructureConfig(gtUIBaseConfig):
    """
    The Griptape Google Structure Config
    """

    def create(
        self,
    ):
        custom_config = GoogleStructureConfig()

        return (custom_config,)


class gtUIAnthropicStructureConfig(gtUIBaseConfig):
    """
    The Griptape Anthropic Structure Config
    """

    def create(
        self,
    ):
        custom_config = AnthropicStructureConfig()
        custom_config.image_query_driver = AnthropicImageQueryDriver(
            model="claude-3-opus-20240229"
        )

        return (custom_config,)


class gtUIOpenAiStructureConfig(gtUIBaseConfig):
    """
    The Griptape OpenAI Structure Config
    """

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    ["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
                    {"default": "gpt-4o"},
                ),
                "image_query_model": (
                    ["gpt-4o", "gpt-4-vision-preview"],
                    {"default": "gpt-4o"},
                ),
            }
        )
        return inputs

    def create(self, prompt_model, image_query_model):
        OPENAI_API_KEY = get_config("env.OPENAI_API_KEY")
        custom_config = StructureConfig(
            prompt_driver=OpenAiChatPromptDriver(
                model=prompt_model, api_key=OPENAI_API_KEY
            ),
            embedding_driver=OpenAiEmbeddingDriver(api_key=OPENAI_API_KEY),
            image_generation_driver=OpenAiImageGenerationDriver(
                api_key=OPENAI_API_KEY,
                model="dalle-e-3",
            ),
            image_query_driver=OpenAiImageQueryDriver(
                api_key=OPENAI_API_KEY, model=image_query_model
            ),
        )

        return (custom_config,)
