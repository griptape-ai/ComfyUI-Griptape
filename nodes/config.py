from griptape.config import (
    AmazonBedrockStructureConfig,
    AnthropicStructureConfig,
    GoogleStructureConfig,
    StructureConfig,
    StructureGlobalDriversConfig,
)
from griptape.drivers import (
    OpenAiChatPromptDriver,
    OpenAiEmbeddingDriver,
    OpenAiImageGenerationDriver,
    OpenAiVisionImageQueryDriver,
)

from ..py.griptape_config import get_config
from .base_config import gtUIBaseConfig


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
                    ["gpt-4o", "clip-vit-base"],
                    {"default": "gpt-4o"},
                ),
            }
        )
        return inputs

    def create(self, prompt_model, image_query_model):
        OPENAI_API_KEY = get_config("env.OPENAI_API_KEY")
        custom_config = StructureConfig(
            global_drivers=StructureGlobalDriversConfig(
                prompt_driver=OpenAiChatPromptDriver(
                    model=prompt_model, api_key=OPENAI_API_KEY
                ),
                embedding_driver=OpenAiEmbeddingDriver(api_key=OPENAI_API_KEY),
                image_generation_driver=OpenAiImageGenerationDriver(
                    api_key=OPENAI_API_KEY,
                    model="dalle-e-3",
                ),
                image_query_driver=OpenAiVisionImageQueryDriver(
                    api_key=OPENAI_API_KEY, model=image_query_model
                ),
            )
        )

        return (custom_config,)
