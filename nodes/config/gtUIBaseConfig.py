import os

from griptape.configs import Defaults
from griptape.configs.drivers import OpenAiDriversConfig

from ..gtUIBase import gtUIBase


class gtUIBaseConfig(gtUIBase):
    """
    Griptape Base Config
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
        return os.getenv(env, None)

    def create(self, **kwargs):
        Defaults.drivers_config = OpenAiDriversConfig()
        return (OpenAiDriversConfig(),)
