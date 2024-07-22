import os

from griptape.config import (
    OpenAiStructureConfig,
)


class gtUIBaseConfig:
    """
    Griptape Base Config
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "temperature": (
                    "FLOAT",
                    {"default": 0.1, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "seed": ("INT", {"default": 10342349342}),
                "max_attempts_on_fail": (
                    "INT",
                    {"default": 10, "min": 1, "max": 100},
                ),
                "stream": ([True, False], {"default": False}),
            },
        }

    RETURN_TYPES = ("CONFIG",)
    RETURN_NAMES = ("CONFIG",)
    FUNCTION = "create"

    # OUTPUT_NODE = False

    CATEGORY = "Griptape/Agent Configs"

    def getenv(self, env):
        return os.getenv(env, None)

    def create(self, **kwargs):
        return (OpenAiStructureConfig(),)
