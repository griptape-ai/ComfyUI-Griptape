from griptape.config import (
    AmazonBedrockStructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AmazonBedrockPromptDriver,
)

from .gtUIBaseConfig import gtUIBaseConfig

amazonBedrockPromptModels = [
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "amazon.titan-text-premier-v1:0",
    "amazon.titan-text-express-v1",
    "amazon.titan-text-lite-v1",
]
amazonBedrockImageGenerationModels = []

DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


class gtUIAmazonBedrockStructureConfig(gtUIBaseConfig):
    """
    The Griptape Amazon Bedrock Structure Config
    """

    DESCRIPTION = "Amazon Bedrock Prompt Driver."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    amazonBedrockPromptModels,
                    {"default": amazonBedrockPromptModels[0]},
                ),
            },
        )
        inputs["optional"].update(
            {
                "aws_access_key_id_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_ACCESS_KEY_ID},
                ),
                "aws_secret_access_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_SECRET_ACCESS_KEY},
                ),
                "aws_default_region_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_DEFAULT_REGION},
                ),
            }
        )
        return inputs

    def create(
        self,
        **kwargs,
    ):
        prompt_model = kwargs.get("prompt_model", amazonBedrockPromptModels[0])
        temperature = kwargs.get("temperature", 0.7)
        max_attempts = kwargs.get("max_attempts_on_fail", 10)

        custom_config = AmazonBedrockStructureConfig(
            prompt_driver=AmazonBedrockPromptDriver(
                model=prompt_model, temperature=temperature, max_attempts=max_attempts
            )
        )
        return (custom_config,)
