from griptape.drivers import BasePromptDriver

from .gtUIBaseDriver import gtUIBaseDriver


class gtUIBasePromptDriver(gtUIBaseDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "model": ((), {"tooltip": "The prompt model to use"}),
                "max_attempts_on_fail": (
                    "INT",
                    {"default": 10, "min": 1, "max": 100},
                ),
                "temperature": (
                    "FLOAT",
                    {"default": 0.1, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "seed": ("INT", {"default": 10342349342}),
                "use_native_tools": ("BOOLEAN", {"default": True}),
                "max_tokens": (
                    "INT",
                    {
                        "default": -1,
                        "tooltip": "Maximum tokens to generate. If <=0, it will use the default based on the tokenizer.",
                    },
                ),
            },
        )
        return inputs

    RETURN_TYPES = ("PROMPT_DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Drivers/Prompt"

    def create(self, **kwargs):
        driver = BasePromptDriver()
        return (driver,)
