from griptape.drivers import BaseTextToSpeechDriver


class gtUIBaseTextToSpeechDriver:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "model": ("STRING", {"default": "eleven_multilingual_v2"}),
                "voice": ("STRING", {"default": "Matilda"}),
            },
        }

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Audio Drivers"

    def create(self, **kwargs):
        model = kwargs.get("model", "eleven_multilingual_v2")
        voice = kwargs.get("voice", "Matilda")
        driver = BaseTextToSpeechDriver(model=model, voice=voice)
        return (driver,)