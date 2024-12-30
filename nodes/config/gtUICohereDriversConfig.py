from griptape.configs import Defaults
from griptape.configs.drivers import (
    CohereDriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    CohereEmbeddingDriver,
    CoherePromptDriver,
    LocalVectorStoreDriver,
)

from ..drivers.gtUICohereEmbeddingDriver import gtUICohereEmbeddingDriver
from ..drivers.gtUICoherePromptDriver import gtUICoherePromptDriver
from .gtUIBaseDriversConfig import (
    add_optional_inputs,
    add_required_inputs,
    gtUIBaseDriversConfig,
)

# Define the list of drivers
drivers = [
    ("prompt", gtUICoherePromptDriver),
    ("embedding", gtUICohereEmbeddingDriver),
]


class gtUICohereDriversConfig(gtUIBaseDriversConfig):
    """
    The Griptape OpenAI Structure Config
    """

    DESCRIPTION = "OpenAI Structure Config. Use OpenAI's models for prompt, embedding, image generation, and image query."

    @classmethod
    def INPUT_TYPES(cls):
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
        prompt_driver_builder = gtUICoherePromptDriver()
        embedding_driver_builder = gtUICohereEmbeddingDriver()

        # Build parameters for drivers
        prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
        embedding_driver_params = embedding_driver_builder.build_params(**kwargs)

        # Create Driver Configs
        drivers_config_params["prompt_driver"] = CoherePromptDriver(
            **prompt_driver_params
        )
        drivers_config_params["embedding_driver"] = CohereEmbeddingDriver(
            **embedding_driver_params
        )
        drivers_config_params["vector_store_driver"] = LocalVectorStoreDriver(
            embedding_driver=drivers_config_params["embedding_driver"]
        )
        drivers_config_params["api_key"] = prompt_driver_params["api_key"]
        try:
            Defaults.drivers_config = CohereDriversConfig(**drivers_config_params)
            custom_config = Defaults.drivers_config
        except Exception as e:
            raise Exception(f"Error creating OpenAiStructureConfig: {e}")

        return (custom_config,)
