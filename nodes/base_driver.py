from griptape.drivers import OpenAiAudioTranscriptionDriver, OpenAiImageGenerationDriver


class gtUIBaseAudioTranscriptionDriver:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {},
        }

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Audio Drivers"

    def create(
        self,
    ):
        driver = OpenAiAudioTranscriptionDriver(model="whisper-1")
        return (driver,)


class gtUIBaseImageGenerationDriver:
    """
    Griptape Base Image Generation Driver
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {},
            "hidden": {"prompt": "PROMPT"},
        }

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Image Drivers"

    def create(self, prompt):
        driver = OpenAiImageGenerationDriver(
            model="dall-e-3", quality="hd", style="natural"
        )
        return (driver,)
