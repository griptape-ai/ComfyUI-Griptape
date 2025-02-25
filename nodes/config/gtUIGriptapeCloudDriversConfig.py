# pyright: reportMissingImports=false
import logging

from comfy_execution.graph import ExecutionBlocker
from griptape.configs import Defaults
from griptape.configs.drivers import (
    DriversConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers.prompt.griptape_cloud import GriptapeCloudPromptDriver

from ..drivers.gtUIGriptapeCloudPromptDriver import gtUIGriptapeCloudPromptDriver
from .gtUIBaseDriversConfig import (
    add_optional_inputs,
    add_required_inputs,
    gtUIBaseDriversConfig,
)

drivers = [
    ("prompt", gtUIGriptapeCloudPromptDriver),
]


class gtUIGriptapeCloudDriversConfig(gtUIBaseDriversConfig):
    """
    The Griptape Cloud Structure Config
    """

    DESCRIPTION = "Griptape Cloud Driver Configs. Griptape Cloud requires a GT_CLOUD_API_KEY available at https://cloud.griptape.ai"

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
            prompt_driver_builder = gtUIGriptapeCloudPromptDriver()

            # Build parameters for drivers
            prompt_driver_params = prompt_driver_builder.build_params(**kwargs)
            if "model" not in prompt_driver_params:
                custom_config = ExecutionBlocker(
                    "Please provide a model for the prompt driver."
                )
                return (custom_config,)

            # Create Driver Configs
            drivers_config_params["prompt_driver"] = GriptapeCloudPromptDriver(
                **prompt_driver_params
            )
            Defaults.drivers_config = DriversConfig(**drivers_config_params)
            custom_config = Defaults.drivers_config
        except Exception as e:
            custom_config = ExecutionBlocker(f"{e}")
            logging.error(e)

        return (custom_config,)
