from griptape.drivers import ElevenLabsTextToSpeechDriver

from ...py.griptape_config import get_config
from .BaseTextToSpeechDriver import gtUIBaseTextToSpeechDriver

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

    CATEGORY = "Griptape/Audio Drivers"

    def create(self, **kwargs):
        api_key = get_config(key="env.ELEVEN_LABS_API_KEY", default=None)

        model = kwargs.get("model", "eleven_multilingual_v2")
        voice = kwargs.get("voice", "Matilda")
        driver = ElevenLabsTextToSpeechDriver(api_key=api_key, model=model, voice=voice)
        return (driver,)
