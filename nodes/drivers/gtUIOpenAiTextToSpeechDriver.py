from griptape.drivers import OpenAiTextToSpeechDriver

from ..utils.openai_utils import get_available_models
from .gtUIBaseTextToSpeechDriver import gtUIBaseTextToSpeechDriver

voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
models = get_available_models("SpeechModel")
default_model = "tts-1"

DEFAULT_API_KEY = "OPENAI_API_KEY"


class gtUIOpenAiTextToSpeechDriver(gtUIBaseTextToSpeechDriver):
    DESCRIPTION = "Griptape OpenAi Text to Speech Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "text_to_speech_model": (
                    models,
                    {
                        "default": models[0],
                        "tooltip": "Enter the text-to-speech model name.",
                    },
                ),
                "voice": (
                    voices,
                    {
                        "default": voices[0],
                        "tooltip": "Select the voice for text-to-speech.",
                    },
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY,
                        "tooltip": "Enter the environment variable name for the API key, not the actual API key.",
                    },
                ),
            }
        )
        return inputs

    FUNCTION = "create"

    def build_params(self, **kwargs):
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))
        model = kwargs.get("text_to_speech_model", models[0])
        voice = kwargs.get("voice", voices[0])

        params = {}
        if api_key:
            params["api_key"] = api_key
        if voice:
            params["voice"] = voice
        if model:
            params["model"] = model
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = OpenAiTextToSpeechDriver(**params)
        return (driver,)
