from typing import Any, Tuple

from griptape.drivers.prompt.dummy import DummyPromptDriver

from .gtUIBaseDriver import gtUIBaseDriver


class gtUIBasePromptDriver(gtUIBaseDriver):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "model": ("STRING", {"tooltip": "The prompt model to use"}),
                "max_attempts_on_fail": (
                    "INT",
                    {
                        "default": 2,
                        "min": 1,
                        "max": 100,
                        "tooltip": "Maximum attempts on failure",
                    },
                ),
                "temperature": (
                    "FLOAT",
                    {
                        "default": 0.1,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.01,
                        "tooltip": "Temperature for sampling",
                    },
                ),
                "seed": (
                    "INT",
                    {
                        "default": 10342349342,
                        "tooltip": "Seed for random number generation",
                    },
                ),
                "use_native_tools": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "Use native tools for the LLM.",
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
        )
        return inputs

    RETURN_TYPES = ("PROMPT_DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Drivers/Prompt"

    def create(self, **kwargs) -> Tuple[Any, ...]:
        driver = DummyPromptDriver()
        return (driver,)
