from griptape.drivers import (
    OpenAiChatPromptDriver,
    OpenAiEmbeddingDriver,
    OpenAiImageGenerationDriver,
    OpenAiVisionImageQueryDriver,
    AmazonBedrockPromptDriver,
    AmazonBedrockImageGenerationDriver,
    AmazonBedrockImageQueryDriver,
    BedrockClaudeImageQueryModelDriver,
    BedrockTitanPromptModelDriver,
    BedrockTitanImageGenerationModelDriver,
    AmazonBedrockTitanEmbeddingDriver,
)
from .base_config import gtUIBaseConfig

from griptape.config import (
    StructureConfig,
    StructureGlobalDriversConfig,
    AmazonBedrockStructureConfig,
    GoogleStructureConfig,
    AnthropicStructureConfig,
)
from ..py.griptape_config import get_config


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
                "model": (["gpt-4", "gpt-3.5-turbo"], {"default": "gpt-4"}),
            }
        )
        return inputs

    def create(self, model):
        OPENAI_API_KEY = get_config("env.OPENAI_API_KEY")
        custom_config = StructureConfig(
            global_drivers=StructureGlobalDriversConfig(
                prompt_driver=OpenAiChatPromptDriver(
                    model=model, api_key=OPENAI_API_KEY
                ),
                embedding_driver=OpenAiEmbeddingDriver(api_key=OPENAI_API_KEY),
                image_generation_driver=OpenAiImageGenerationDriver(
                    api_key=OPENAI_API_KEY,
                    model="text-davinci-003",
                ),
                image_query_driver=OpenAiVisionImageQueryDriver(
                    api_key=OPENAI_API_KEY, model="clip-vit-base"
                ),
            )
        )

        return (custom_config,)
