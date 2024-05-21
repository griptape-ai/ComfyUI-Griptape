from griptape.drivers import OpenAiChatPromptDriver
from griptape.engines import BaseExtractionEngine


class gtUIBaseExtractionEngine:
    """
    Griptape Base Image Generation Driver
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "prompt_driver": (
                    "DRIVER",
                    {
                        "default": OpenAiChatPromptDriver(model="gpt-3.5-turbo"),
                        "forceInput": True,
                    },
                ),
                "max_token_multiplier": ("FLOAT", {"default": 0.5}),
                "chunk_joiner": ("STRING", {"default": "\n\n"}),
            },
            "hidden": {"prompt": "PROMPT"},
        }

    RETURN_TYPES = ("ENGINE",)
    RETURN_NAMES = ("ENGINE",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Engines"

    def create(self, **kwargs):
        prompt_driver = kwargs.get("prompt_driver")
        max_token_multiplier = kwargs.get("max_token_multiplier")
        chunk_joiner = kwargs.get("chunk_joiner")

        engine = BaseExtractionEngine(
            driver=prompt_driver,
            max_token_multiplier=max_token_multiplier,
            chunk_joiner=chunk_joiner,
        )

        return (engine,)
