# pyright: reportMissingImports=false
import logging

from comfy_execution.graph import ExecutionBlocker
from griptape.configs import Defaults
from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers.embedding.dummy import DummyEmbeddingDriver
from griptape.drivers.embedding.openai import OpenAiEmbeddingDriver
from griptape.drivers.prompt.openai import OpenAiChatPromptDriver
from griptape.drivers.vector.local import LocalVectorStoreDriver

from ..drivers.gtUILMStudioChatPromptDriver import gtUILMStudioChatPromptDriver
from ..drivers.gtUILMStudioEmbeddingDriver import gtUILMStudioEmbeddingDriver
from .gtUIBaseDriversConfig import (
    add_optional_inputs,
    add_required_inputs,
    gtUIBaseDriversConfig,
)

drivers = [
    ("prompt", gtUILMStudioChatPromptDriver),
    ("embedding", gtUILMStudioEmbeddingDriver),
]


class gtUILMStudioDriversConfig(gtUIBaseDriversConfig):
    """
    The Griptape LM Studio Structure Config
    """

    DESCRIPTION = (
        "LM Studio Prompt Driver. LMStudio is available at https://lmstudio.ai "
    )

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"] = {}

        inputs = add_required_inputs(inputs, drivers)
        inputs = add_optional_inputs(inputs, drivers)

        return inputs

    def create(self, **kwargs):
        drivers_config_params = {}

        try:
            # Create instances of the driver classes
            prompt_driver_builder = gtUILMStudioChatPromptDriver()
            embedding_driver_builder = gtUILMStudioEmbeddingDriver()

            # Build parameters for drivers
            prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
            embedding_driver_params = embedding_driver_builder.build_params(**kwargs)
            if "model" not in prompt_driver_params:
                custom_config = ExecutionBlocker(
                    "Please provide a model for the prompt driver."
                )
                return (custom_config,)
            # Create Driver Configs
            drivers_config_params["prompt_driver"] = OpenAiChatPromptDriver(
                **prompt_driver_params
            )
            if "model" not in embedding_driver_params:
                drivers_config_params["embedding_driver"] = DummyEmbeddingDriver()
            else:
                drivers_config_params["embedding_driver"] = OpenAiEmbeddingDriver(
                    **embedding_driver_params
                )

            drivers_config_params["vector_store_driver"] = LocalVectorStoreDriver(
                embedding_driver=drivers_config_params["embedding_driver"]
            )
            Defaults.drivers_config = DriversConfig(**drivers_config_params)
            custom_config = Defaults.drivers_config
        except Exception as e:
            custom_config = ExecutionBlocker(f"{e}")
            logging.error(e)

        return (custom_config,)
