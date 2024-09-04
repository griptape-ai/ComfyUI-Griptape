from griptape.configs import Defaults
from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    LocalVectorStoreDriver,
    OpenAiChatPromptDriver,
    OpenAiEmbeddingDriver,
)

from ..drivers.gtUILMStudioChatPromptDriver import gtUILMStudioChatPromptDriver
from ..drivers.gtUILMStudioEmbeddingDriver import gtUILMStudioEmbeddingDriver
from .gtUIBaseConfig import add_optional_inputs, add_required_inputs, gtUIBaseConfig

drivers = [
    ("prompt", gtUILMStudioChatPromptDriver),
    ("embedding", gtUILMStudioEmbeddingDriver),
]


class gtUILMStudioStructureConfig(gtUIBaseConfig):
    """
    The Griptape LM Studio Structure Config
    """

    DESCRIPTION = (
        "LM Studio Prompt Driver. LMStudio is available at https://lmstudio.ai "
    )

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"] = {}

        inputs = add_required_inputs(inputs, drivers)
        inputs = add_optional_inputs(inputs, drivers)

        return inputs

    def create(self, **kwargs):
        drivers_config_params = {}

        # Create instances of the driver classes
        prompt_driver_builder = gtUILMStudioChatPromptDriver()
        embedding_driver_builder = gtUILMStudioEmbeddingDriver()

        # Build parameters for drivers
        prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
        embedding_driver_params = embedding_driver_builder.build_params(**kwargs)

        # Create Driver Configs
        drivers_config_params["prompt_driver"] = OpenAiChatPromptDriver(
            **prompt_driver_params
        )
        drivers_config_params["embedding_driver"] = OpenAiEmbeddingDriver(
            **embedding_driver_params
        )

        drivers_config_params["vector_store_driver"] = LocalVectorStoreDriver(
            embedding_driver=OpenAiEmbeddingDriver(**embedding_driver_params)
        )

        try:
            Defaults.drivers_config = DriversConfig(**drivers_config_params)
            custom_config = Defaults.drivers_config
        except Exception as e:
            print(e)

        return (custom_config,)
