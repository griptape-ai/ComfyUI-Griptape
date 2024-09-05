from griptape.drivers import BaseTextToSpeechDriver

from .gtUIBaseDriver import gtUIBaseDriver


class gtUIBaseTextToSpeechDriver(gtUIBaseDriver):
    DESCRIPTION = "Griptape Text to Speech Driver"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "text_to_speech_model": (
                    "STRING",
                    {"default": "eleven_multilingual_v2"},
                ),
                "voice": ("STRING", {"default": "Matilda"}),
            },
        }

    RETURN_TYPES = ("TEXT_TO_SPEECH_DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Drivers/Text to Speech"

    def create(self, **kwargs):
        model = kwargs.get("text_to_speech_model", "eleven_multilingual_v2")
        voice = kwargs.get("voice", "Matilda")
        driver = BaseTextToSpeechDriver(model=model, voice=voice)
        return (driver,)
