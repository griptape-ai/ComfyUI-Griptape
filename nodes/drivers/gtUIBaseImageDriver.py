from griptape.drivers import OpenAiImageGenerationDriver

from .gtUIBaseDriver import gtUIBaseDriver

DEFAULT_API_KEY = "OPENAI_API_KEY"
DEFAULT_MODEL = "dall-e-3"
DEFAULT_QUALITY = "hd"
DEFAULT_STYLE = "natural"


class gtUIBaseImageGenerationDriver(gtUIBaseDriver):
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

    CATEGORY = "Griptape/Drivers/Image Generation"

    def create(self, prompt):
        api_key = self.getenv(DEFAULT_API_KEY)
        params = {}
        if api_key:
            params["api_key"] = api_key
        params["model"] = DEFAULT_MODEL
        params["quality"] = DEFAULT_QUALITY
        params["style"] = DEFAULT_STYLE

        driver = OpenAiImageGenerationDriver(**params)
        return (driver,)
