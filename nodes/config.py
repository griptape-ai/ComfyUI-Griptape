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
from griptape.config import (
    StructureConfig,
    StructureGlobalDriversConfig,
    OpenAiStructureConfig,
    AmazonBedrockStructureConfig,
    GoogleStructureConfig,
    AnthropicStructureConfig,
)
from ..py.griptape_config import get_config

from groq import Groq
import boto3
import os


# def get_env_variables():
#     """
#     Get environment variables
#     """
#     env_variables = ""
#     required_envs = [
#         "OPENAI_API_KEY",
#         "AZURE_OPENAI_API_KEY",
#         "AZURE_OPENAI_GPT_4_DEPLOYMENT_ID",
#         "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME",
#         "AZURE_OPENAI_EMBEDDING_MODEL_NAME",
#         "AZURE_OPENAI_PROMPT_DEPLOYMENT_NAME",
#         "AZURE_OPENAI_PROMPT_MODEL_NAME",
#         "AZURE_OPENAI_ENDPOINT",
#         "AWS_ACCESS_KEY_ID",
#         "AWS_SECRET_ACCESS_KEY",
#         "LEONARDO_API_KEY",
#         "GROQ_API_KEY",
#     ]
#     for env in required_envs:
#         env_variables += f"{env}={os.getenv(env)}\n"
#     return env_variables


# class gtUIEnvironmentConfig:
#     """
#     Griptape Environment Config
#     """

#     def __init__(self):
#         pass

#     @classmethod
#     def INPUT_TYPES(s):
#         # get relevant environment variables
#         open_ai_api_key =
#         open_ai_api_key = os.getenv("OPENAI_API_KEY")

#         return {
#             "required": {
#                 "env": (
#                     "STRING",
#                     {"multiline": True, "default": get_env_variables()},
#                 ),
#             }
#         }

#     # INPUT_AS_LIST = True
#     RETURN_TYPES = ("",)
#     # RETURN_NAMES = ("CONFIG",)
#     FUNCTION = "create"

#     OUTPUT_NODE = True

#     CATEGORY = "Griptape/Config"

#     def create(
#         self,
#         env,
#     ):
#         for line in env.split("\n"):
#             if "=" not in line:
#                 continue
#             key, value = line.split("=")
#             os.putenv(key.strip(), value.strip())
#         return ((),)


class gtUIBaseConfig:
    """
    Griptape Base Config
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}, "optional": {}}

    RETURN_TYPES = ("CONFIG",)
    RETURN_NAMES = ("CONFIG",)
    FUNCTION = "create"

    # OUTPUT_NODE = False

    CATEGORY = "Griptape/Config"

    def create(
        self,
    ):
        return (OpenAiStructureConfig(),)


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
        # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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


# # Create different models
# gpt_4 = OpenAiStructureConfig()


# gpt_35 = StructureConfig(
#     global_drivers=StructureGlobalDriversConfig(
#         prompt_driver=OpenAiChatPromptDriver(model="gpt-3.5-turbo"),
#         embedding_driver=OpenAiEmbeddingDriver(),
#     )
# )
