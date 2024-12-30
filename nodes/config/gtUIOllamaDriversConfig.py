from griptape.configs import Defaults
from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    DummyEmbeddingDriver,
    LocalVectorStoreDriver,
    OllamaEmbeddingDriver,
    OllamaPromptDriver,
)

from ..drivers.gtUIOllamaEmbeddingDriver import gtUIOllamaEmbeddingDriver
from ..drivers.gtUIOllamaPromptDriver import gtUIOllamaPromptDriver
from .gtUIBaseDriversConfig import (
    add_optional_inputs,
    add_required_inputs,
    gtUIBaseDriversConfig,
)

drivers = [
    ("prompt", gtUIOllamaPromptDriver),
    ("embedding", gtUIOllamaEmbeddingDriver),
]


class gtUIOllamaDriversConfig(gtUIBaseDriversConfig):
    """
    The Griptape Ollama Structure Config
    """

    DESCRIPTION = "Ollama Prompt Driver. Use local models with Ollama. Available at https://ollama.com"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"] = {}

        inputs = add_required_inputs(inputs, drivers)
        inputs = add_optional_inputs(inputs, drivers)

        return inputs

    def create(self, **kwargs):
        self.run_envs(kwargs)
        custom_config = None

        drivers_config_params = {}

        # Create instances of the driver classes
        prompt_driver_builder = gtUIOllamaPromptDriver()
        embedding_driver_builder = gtUIOllamaEmbeddingDriver()

        # Build parameters for drivers
        prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
        embedding_driver_params = embedding_driver_builder.build_params(**kwargs)

        # Create driver configs
        drivers_config_params["prompt_driver"] = OllamaPromptDriver(
            **prompt_driver_params
        )
        if "model" not in embedding_driver_params:
            drivers_config_params["embedding_driver"] = DummyEmbeddingDriver()
        else:
            drivers_config_params["embedding_driver"] = OllamaEmbeddingDriver(
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
