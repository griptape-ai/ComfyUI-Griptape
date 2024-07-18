import os

from griptape.drivers import OpenAiTextToSpeechDriver

from .gtUIBaseTextToSpeechDriver import gtUIBaseTextToSpeechDriver

voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
default_model = "tts-1"


class gtUIOpenAiTextToSpeechDriver(gtUIBaseTextToSpeechDriver):
    DESCRIPTION = "Griptape OpenAi Text to Speech Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "model": ("STRING", {"default": default_model}),
                "voice": (voices, {"default": voices[0]}),
            }
        )
        return inputs

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    def create(self, **kwargs):
        api_key = os.getenv("OPENAI_API_KEY")
        model = kwargs.get("model", default_model)
        voice = kwargs.get("voice", voices[0])

        params = {}
        if api_key:
            params["api_key"] = api_key
        if voice:
            params["voice"] = voice
        if model:
            params["model"] = model
        driver = OpenAiTextToSpeechDriver(**params)
        return (driver,)
