from griptape.drivers import OpenAiImageGenerationDriver


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
