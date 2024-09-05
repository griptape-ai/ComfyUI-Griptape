from griptape.configs import Defaults
from griptape.configs.drivers import (
    AmazonBedrockDriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AmazonBedrockImageGenerationDriver,
    AmazonBedrockPromptDriver,
    AmazonBedrockTitanEmbeddingDriver,
    LocalVectorStoreDriver,
)

from ..drivers.gtUIAmazonBedrockPromptDriver import gtUIAmazonBedrockPromptDriver
from ..drivers.gtUIAmazonBedrockTitanEmbeddingDriver import (
    gtUIAmazonBedrockTitanEmbeddingDriver,
)
from ..drivers.gtUIAmazonBedrockTitanImageGenerationDriver import (
    gtUIAmazonBedrockTitanImageGenerationDriver,
)
from .gtUIBaseDriversConfig import (
    add_optional_inputs,
    add_required_inputs,
    gtUIBaseDriversConfig,
)

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


# Define the list of drivers
drivers = [
    ("prompt", gtUIAmazonBedrockPromptDriver),
    ("embedding", gtUIAmazonBedrockTitanEmbeddingDriver),
    ("image_generation", gtUIAmazonBedrockTitanImageGenerationDriver),
]


class gtUIAmazonBedrockDriversConfig(gtUIBaseDriversConfig):
    """
    The Griptape Amazon Bedrock Structure Config
    """

    DESCRIPTION = "Amazon Bedrock Prompt Driver."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"] = {}

        inputs = add_required_inputs(inputs, drivers)
        inputs = add_optional_inputs(inputs, drivers)

        return inputs

    def create(
        self,
        **kwargs,
    ):
        self.run_envs(kwargs)
        drivers_config_params = {}

        # Create instances of the driver classes
        prompt_driver_builder = gtUIAmazonBedrockPromptDriver()
        embedding_driver_builder = gtUIAmazonBedrockTitanEmbeddingDriver()
        image_generation_driver_builder = gtUIAmazonBedrockTitanImageGenerationDriver()

        # Build parameters for drivers
        prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
        embedding_driver_params = embedding_driver_builder.build_params(**kwargs)
        image_generation_driver_params = image_generation_driver_builder.build_params(
            **kwargs
        )

        for name in ["aws_access_key_id", "aws_secret_access_key", "region_name"]:
            prompt_driver_params.pop(name)
            embedding_driver_params.pop(name)
            image_generation_driver_params.pop(name)

        # Create Driver Configs
        drivers_config_params["prompt_driver"] = AmazonBedrockPromptDriver(
            **prompt_driver_params
        )
        drivers_config_params["embedding_driver"] = AmazonBedrockTitanEmbeddingDriver(
            **embedding_driver_params
        )
        drivers_config_params["image_generation_driver"] = (
            AmazonBedrockImageGenerationDriver(**image_generation_driver_params)
        )
        drivers_config_params["vector_store_driver"] = LocalVectorStoreDriver(
            embedding_driver=AmazonBedrockTitanEmbeddingDriver(
                **embedding_driver_params
            )
        )

        try:
            Defaults.drivers_config = AmazonBedrockDriversConfig(
                **drivers_config_params
            )
            custom_config = Defaults.drivers_config
        except Exception as e:
            raise Exception(f"Error creating AmazonBedrockStructureConfig: {e}")

        return (custom_config,)
