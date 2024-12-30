from griptape.configs import Defaults
from griptape.configs.drivers import AzureOpenAiDriversConfig

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AzureOpenAiChatPromptDriver,
    AzureOpenAiEmbeddingDriver,
    AzureOpenAiImageGenerationDriver,
    LocalVectorStoreDriver,
)

from ..drivers.gtUIAzureOpenAiChatPromptDriver import gtUIAzureOpenAiChatPromptDriver
from ..drivers.gtUIAzureOpenAiEmbeddingDriver import gtUIAzureOpenAiEmbeddingDriver
from ..drivers.gtUIAzureOpenAiImageGenerationDriver import (
    gtUIAzureOpenAiImageGenerationDriver,
)
from .gtUIBaseDriversConfig import (
    add_optional_inputs,
    add_required_inputs,
    gtUIBaseDriversConfig,
)

DEFAULT_AZURE_OPENAI_ENDPOINT = "AZURE_OPENAI_ENDPOINT"
DEFAULT_AZURE_OPENAI_API_KEY = "AZURE_OPENAI_API_KEY"
# Define the list of drivers
drivers = [
    ("prompt", gtUIAzureOpenAiChatPromptDriver),
    ("image_generation", gtUIAzureOpenAiImageGenerationDriver),
    ("embedding", gtUIAzureOpenAiEmbeddingDriver),
]


class gtUIAzureOpenAiDriversConfig(gtUIBaseDriversConfig):
    """
    The Griptape OpenAI Structure Config
    """

    DESCRIPTION = "Azure OpenAI Structure Config. Requires AZURE_OPENAI_ENDPOINT_3 and AZURE_OPENAI_API_KEY_3"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["optional"] = {}

        inputs = add_required_inputs(inputs, drivers)
        inputs = add_optional_inputs(inputs, drivers)

        return inputs

    def create(self, **kwargs):
        self.run_envs(kwargs)
        drivers_config_params = {}

        # Create instances of the driver classes
        prompt_driver_builder = gtUIAzureOpenAiChatPromptDriver()
        embedding_driver_builder = gtUIAzureOpenAiEmbeddingDriver()
        image_generation_driver_builder = gtUIAzureOpenAiImageGenerationDriver()

        # Build parameters for drivers
        prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
        embedding_driver_params = embedding_driver_builder.build_params(**kwargs)
        image_generation_driver_params = image_generation_driver_builder.build_params(
            **kwargs
        )

        # Create Driver Configs
        drivers_config_params["prompt_driver"] = AzureOpenAiChatPromptDriver(
            **prompt_driver_params
        )
        drivers_config_params["embedding_driver"] = AzureOpenAiEmbeddingDriver(
            **embedding_driver_params
        )
        drivers_config_params["image_generation_driver"] = (
            AzureOpenAiImageGenerationDriver(**image_generation_driver_params)
        )
        drivers_config_params["vector_store_driver"] = LocalVectorStoreDriver(
            embedding_driver=AzureOpenAiEmbeddingDriver(**embedding_driver_params)
        )
        drivers_config_params["azure_endpoint"] = prompt_driver_params["azure_endpoint"]
        drivers_config_params["api_key"] = prompt_driver_params["api_key"]

        try:
            Defaults.drivers_config = AzureOpenAiDriversConfig(**drivers_config_params)
            custom_config = Defaults.drivers_config
        except Exception as e:
            raise e
            return (None,)

        return (custom_config,)
