from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    OllamaEmbeddingDriver,
    OllamaPromptDriver,
)

from ..drivers.gtUIOllamaEmbeddingDriver import gtUIOllamaEmbeddingDriver
from ..drivers.gtUIOllamaPromptDriver import gtUIOllamaPromptDriver
from .gtUIBaseConfig import gtUIBaseConfig

ollama_port = "11434"
ollama_base_url = "http://127.0.0.1"


class gtUIOllamaStructureConfig(gtUIBaseConfig):
    """
    The Griptape Ollama Structure Config
    """

    DESCRIPTION = "Ollama Prompt Driver. Use local models with Ollama. Available at https://ollama.com"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        optional_inputs = inputs["optional"]

        # Clear optional inputs
        inputs["optional"] = {}

        # add required inputs from each driver
        inputs["required"].update(gtUIOllamaPromptDriver.INPUT_TYPES()["required"])
        inputs["required"].update(gtUIOllamaEmbeddingDriver.INPUT_TYPES()["required"])

        # add optional inputs from each driver, and include a comment for each
        inputs["optional"].update(
            {
                "prompt_model_comment": (
                    "STRING",
                    {
                        "default": "Prompt Model",
                    },
                ),
            }
        )
        inputs["optional"].update(gtUIOllamaPromptDriver.INPUT_TYPES()["optional"])
        inputs["optional"].update(optional_inputs)

        inputs["optional"].update(
            {
                "embedding_model_comment": (
                    "STRING",
                    {
                        "default": "Embedding Model",
                    },
                ),
            }
        )
        inputs["optional"].update(gtUIOllamaEmbeddingDriver.INPUT_TYPES()["optional"])

        return inputs

    def create(self, **kwargs):
        self.run_envs(kwargs)

        drivers_config_params = {}

        # Create instances of the driver classes
        prompt_driver_builder = gtUIOllamaPromptDriver()
        embedding_driver_builder = gtUIOllamaEmbeddingDriver()

        # Build parameters for prompt driver
        prompt_driver_params = prompt_driver_builder.build_params(**kwargs)

        # Build parameters for embedding driver
        embedding_driver_params = embedding_driver_builder.build_params(**kwargs)

        prompt_driver = OllamaPromptDriver(**prompt_driver_params)

        embedding_driver = OllamaEmbeddingDriver(**embedding_driver_params)

        # Drivers Config Params
        drivers_config_params["prompt_driver"] = prompt_driver
        drivers_config_params["embedding_driver"] = embedding_driver
        custom_config = DriversConfig(**drivers_config_params)

        return (custom_config,)
