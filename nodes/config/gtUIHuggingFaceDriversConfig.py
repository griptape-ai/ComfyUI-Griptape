from dotenv import load_dotenv
from griptape.configs import Defaults
from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    HuggingFaceHubEmbeddingDriver,
    HuggingFaceHubPromptDriver,
    LocalVectorStoreDriver,
)

from ..drivers.gtUIHuggingFaceHubEmbeddingDriver import (
    gtUIHuggingFaceHubEmbeddingDriver,
)
from ..drivers.gtUIHuggingFaceHubPromptDriver import gtUIHuggingFaceHubPromptDriver
from .gtUIBaseDriversConfig import (
    add_optional_inputs,
    add_required_inputs,
    gtUIBaseDriversConfig,
)

load_dotenv()

DEFAULT_API_KEY = "HUGGINGFACE_HUB_ACCESS_TOKEN"

# Define the list of drivers
drivers = [
    ("prompt", gtUIHuggingFaceHubPromptDriver),
    ("embedding", gtUIHuggingFaceHubEmbeddingDriver),
]


class gtUIHuggingFaceDriversConfig(gtUIBaseDriversConfig):
    """
    Create a HuggingFace Structure Config
    """

    DESCRIPTION = "HuggingFace Structure Config."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"] = {}

        inputs = add_required_inputs(inputs, drivers)
        inputs = add_optional_inputs(inputs, drivers)
        return inputs

    def create(self, **kwargs):
        self.run_envs(kwargs)

        drivers_config_params = {}

        # Create instances of the driver classes
        prompt_driver_builder = gtUIHuggingFaceHubPromptDriver()
        embedding_driver_builder = gtUIHuggingFaceHubEmbeddingDriver()

        # Build parameters for drivers
        prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
        embedding_driver_params = embedding_driver_builder.build_params(**kwargs)

        # Create Driver Configs
        drivers_config_params["prompt_driver"] = HuggingFaceHubPromptDriver(
            **prompt_driver_params
        )
        drivers_config_params["embedding_driver"] = HuggingFaceHubEmbeddingDriver(
            **embedding_driver_params
        )
        drivers_config_params["vector_store_driver"] = LocalVectorStoreDriver(
            embedding_driver=drivers_config_params["embedding_driver"]
        )

        try:
            Defaults.drivers_config = DriversConfig(**drivers_config_params)
            custom_config = Defaults.drivers_config
        except Exception as e:
            print(e)

        return (custom_config,)
