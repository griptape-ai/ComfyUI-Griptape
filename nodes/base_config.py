from griptape.config import (
    OpenAiStructureConfig,
)
from ..py.griptape_config import get_config


class gtUIBaseConfig:
    """
    Griptape Base Config
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}, "optional": {}}

    RETURN_TYPES = ("CONFIG",)
    RETURN_NAMES = ("CONFIG",)
    FUNCTION = "create"

    # OUTPUT_NODE = False

    CATEGORY = "Griptape/Agent Config"

    def create(
        self,
    ):
        return (OpenAiStructureConfig(),)
