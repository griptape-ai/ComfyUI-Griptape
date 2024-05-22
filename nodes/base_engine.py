from griptape.drivers import OpenAiChatPromptDriver
from griptape.engines import BaseExtractionEngine


class gtUIBaseExtractionEngine:
    """
    Griptape Base Image Generation Driver
    """

    @classmethod
    def INPUT_TYPES(s):
        drivers = ["gpt-4o", "gpt-4", "gpt-3.5-turbo", ""]
        return {
            "required": {},
            "optional": {
                "prompt_driver": (
                    drivers,
                    {
                        "default": drivers[2],
                    },
                ),
                "max_token_multiplier": ("FLOAT", {"default": 0.5}),
                "chunk_joiner": ("STRING", {"default": "\\n\\n"}),
            },
            "hidden": {"prompt": "PROMPT"},
        }

    RETURN_TYPES = ("ENGINE",)
    RETURN_NAMES = ("ENGINE",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Engines"

    def create(self, **kwargs):
        driver = OpenAiChatPromptDriver(model=prompt_driver)
        max_token_multiplier = kwargs.get("max_token_multiplier")
        chunk_joiner = kwargs.get("chunk_joiner")

        engine = BaseExtractionEngine(
            driver=driver,
            max_token_multiplier=max_token_multiplier,
            chunk_joiner=chunk_joiner,
        )

        return (engine,)
