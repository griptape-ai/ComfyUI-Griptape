from griptape.drivers import BasePromptDriver


class gtUIBasePromptDriver:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "stream": ("BOOLEAN", {"default": False}),
                "max_attempts_on_fail": (
                    "INT",
                    {"default": 10, "min": 1, "max": 100},
                ),
                "temperature": (
                    "FLOAT",
                    {"default": 0.1, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "seed": ("INT", {"default": 10342349342}),
            },
        }

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Drivers/Audio Transcription"

    def create(self, **kwargs):
        driver = BasePromptDriver()
        return (driver,)
