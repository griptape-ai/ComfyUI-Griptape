from griptape.configs import Defaults
from griptape.configs.drivers import OpenAiDriversConfig

from ...py.griptape_settings import GriptapeSettings
from ..gtUIBase import gtUIBase


def add_required_inputs(inputs, drivers):
    for _, driver in drivers:
        inputs["required"].update(driver.INPUT_TYPES()["required"])
    return inputs


def add_optional_inputs(inputs, drivers):
    # Add optional inputs and comments for each driver
    for name, driver in drivers:
        inputs["optional"].update(
            {
                f"{name}_model_comment": (
                    "STRING",
                    {"default": f"{name.replace('_', ' ').title()} Driver"},
                ),
            }
        )
        inputs["optional"].update(driver.INPUT_TYPES()["optional"])
    return inputs


class gtUIBaseDriversConfig(gtUIBase):
    """
    Griptape Base Drivers Config
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        return inputs

    RETURN_TYPES = ("CONFIG",)
    RETURN_NAMES = ("CONFIG",)
    FUNCTION = "create"

    # OUTPUT_NODE = False

    CATEGORY = "Griptape/Agent Configs"

    def getenv(self, env):
        settings = GriptapeSettings()
        api_key = settings.get_settings_key_or_use_env(env)
        return api_key

    def create(self, **kwargs):
        Defaults.drivers_config = OpenAiDriversConfig()
        return (OpenAiDriversConfig(),)
