import os

from griptape.drivers import ElevenLabsTextToSpeechDriver

from .gtUIBaseTextToSpeechDriver import gtUIBaseTextToSpeechDriver

premade_voices = []


class gtUIElevenLabsTextToSpeechDriver(gtUIBaseTextToSpeechDriver):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "model": ("STRING", {"default": "eleven_multilingual_v2"}),
                "voice": ("STRING", {"default": "Matilda"}),
            }
        )
        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    def create(self, **kwargs):
        api_key = os.getenv("ELEVEN_LABS_API_KEY")

        model = kwargs.get("model", "eleven_multilingual_v2")
        voice = kwargs.get("voice", "Matilda")
        driver = ElevenLabsTextToSpeechDriver(api_key=api_key, model=model, voice=voice)
        return (driver,)
