from typing import Any, Tuple

from griptape.drivers import DummyTextToSpeechDriver

from .gtUIBaseDriver import gtUIBaseDriver


class gtUIBaseTextToSpeechDriver(gtUIBaseDriver):
    DESCRIPTION = "Griptape Text to Speech Driver"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "text_to_speech_model": (
                    "STRING",
                    {
                        "default": "eleven_multilingual_v2",
                        "tooltip": "Select the text-to-speech model to use.",
                    },
                ),
                "voice": (
                    "STRING",
                    {
                        "default": "Matilda",
                        "tooltip": "Select the voice for the text-to-speech output.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("TEXT_TO_SPEECH_DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Drivers/Text to Speech"

    def create(self, **kwargs) -> Tuple[Any, ...]:
        driver = DummyTextToSpeechDriver()
        return (driver,)
