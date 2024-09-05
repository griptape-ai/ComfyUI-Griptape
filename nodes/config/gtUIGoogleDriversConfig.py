from griptape.configs import Defaults
from griptape.configs.drivers import (
    GoogleDriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    GoogleEmbeddingDriver,
    GooglePromptDriver,
    LocalVectorStoreDriver,
)

from ..drivers.gtUIGoogleEmbeddingDriver import gtUIGoogleEmbeddingDriver
from ..drivers.gtUIGooglePromptDriver import gtUIGooglePromptDriver
from .gtUIBaseDriversConfig import (
    add_optional_inputs,
    add_required_inputs,
    gtUIBaseDriversConfig,
)

google_models = [
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.0-pro",
]

DEFAULT_API_KEY = "GOOGLE_API_KEY"
# Define the list of drivers
drivers = [
    ("prompt", gtUIGooglePromptDriver),
    ("embedding", gtUIGoogleEmbeddingDriver),
]


class gtUIGoogleDriversConfig(gtUIBaseDriversConfig):
    """
    The Griptape Google Structure Config
    """

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"] = {}

        inputs = add_required_inputs(inputs, drivers)
        inputs = add_optional_inputs(inputs, drivers)

        return inputs

    DESCRIPTION = (
        "Google Structure Config. Use Google's models for prompt and image query."
    )

    def create(self, **kwargs):
        self.run_envs(kwargs)

        drivers_config_params = {}
        # Create instances of the driver classes
        prompt_driver_builder = gtUIGooglePromptDriver()
        embedding_driver_builder = gtUIGoogleEmbeddingDriver()

        # Build parameters for drivers
        prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
        embedding_driver_params = embedding_driver_builder.build_params(**kwargs)

        # Create Driver Configs
        drivers_config_params["prompt_driver"] = GooglePromptDriver(
            **prompt_driver_params
        )
        drivers_config_params["embedding_driver"] = GoogleEmbeddingDriver(
            **embedding_driver_params
        )
        drivers_config_params["vector_store_driver"] = LocalVectorStoreDriver(
            embedding_driver=drivers_config_params["embedding_driver"]
        )
        try:
            Defaults.drivers_config = GoogleDriversConfig(**drivers_config_params)
            custom_config = Defaults.drivers_config

        except Exception as e:
            print(e)

        return (custom_config,)
