from griptape.configs import Defaults
from griptape.configs.drivers import AnthropicDriversConfig

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AnthropicPromptDriver,
)

from ..drivers.gtUIAnthropicPromptDriver import gtUIAnthropicPromptDriver
from .gtUIBaseDriversConfig import (
    add_optional_inputs,
    add_required_inputs,
    gtUIBaseDriversConfig,
)

anthropicPromptModels = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

DEFAULT_API_KEY = "ANTHROPIC_API_KEY"

# Define the list of drivers
drivers = [
    ("prompt", gtUIAnthropicPromptDriver),
    # ("embedding", gtUIVoyageAiEmbeddingDriver),
]


class gtUIAnthropicDriversConfig(gtUIBaseDriversConfig):
    """
    The Griptape Anthropic Structure Config
    """

    DESCRIPTION = (
        "Anthropic Structure Config. Use Anthropic's models for prompt and image query."
    )

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
        prompt_driver_builder = gtUIAnthropicPromptDriver()
        # embedding_driver_builder = gtUIVoyageAiEmbeddingDriver()

        # Build parameters for drivers
        prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
        # embedding_driver_params = embedding_driver_builder.build_params(**kwargs)

        # Create Driver Configs
        drivers_config_params["prompt_driver"] = AnthropicPromptDriver(
            **prompt_driver_params
        )

        # if embedding_driver_params == {}:
        #     drivers_config_params["embedding_driver"] = VoyageAiEmbeddingDriver(
        #         **embedding_driver_params
        #     )
        # else:
        #     drivers_config_params["embedding_driver"] = DummyEmbeddingDriver()

        # drivers_config_params["vector_store_driver"] = LocalVectorStoreDriver(
        #     embedding_driver=drivers_config_params["embedding_driver"]
        # )

        try:
            Defaults.drivers_config = AnthropicDriversConfig(**drivers_config_params)
            custom_config = Defaults.drivers_config
        except Exception as e:
            raise Exception(f"Error creating AnthropicDriversConfig: {e}")

        return (custom_config,)
