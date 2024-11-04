from griptape.configs import Defaults
from griptape.configs.drivers import OpenAiDriversConfig

from ...py.griptape_settings import GriptapeSettings


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
                # "stream": ([True, False], {"default": False}),
                "env": ("ENV", {"default": None}),
                "use_native_tools": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "label_on": "True (LLM-native tool calling)",
                        "label_off": "False (Griptape tool calling)",
                    },
                ),
                "max_tokens": (
                    "INT",
                    {
                        "default": -1,
                        "tooltip": "Maximum tokens to generate. If <=0, it will use the default based on the tokenizer.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("CONFIG",)
    RETURN_NAMES = ("CONFIG",)
    FUNCTION = "create"

    # OUTPUT_NODE = False

    CATEGORY = "Griptape/Agent Configs [DEPRICATED]"

    def getenv(self, env):
        settings = GriptapeSettings()
        api_key = settings.get_settings_key_or_use_env(env)
        return api_key

    def create(self, **kwargs):
        Defaults.drivers_config = OpenAiDriversConfig()
        return (OpenAiDriversConfig(),)
