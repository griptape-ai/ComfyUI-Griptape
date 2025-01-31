from typing import get_args

from griptape.drivers import OpenAiAudioTranscriptionDriver
from openai.types import AudioModel

from .gtUIBaseAudioTranscriptionDriver import gtUIBaseAudioTranscriptionDriver

# models = get_available_models("AudioModel")
models = get_args(AudioModel)
DEFAULT_MODEL = ""
if len(models) > 0:
    DEFAULT_MODEL = models[0]

DEFAULT_API_KEY = "OPENAI_API_KEY"


class gtUIOpenAiAudioTranscriptionDriver(gtUIBaseAudioTranscriptionDriver):
    DESCRIPTION = "OpenAI Audio Transcription Driver"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "audio_transcription_model": (
                    models,
                    {
                        "default": DEFAULT_MODEL,
                        "tooltip": "Select the audio transcription model to use.",
                    },
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY,
                        "tooltip": "Enter the name of the environment variable that contains the API key, not the API key itself.",
                    },
                ),
            },
        )

        return inputs

    def build_params(self, **kwargs):
        model = kwargs.get("audio_transcription_model", DEFAULT_MODEL)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))

        params = {}

        if model:
            params["model"] = model
        if api_key:
            params["api_key"] = api_key

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = OpenAiAudioTranscriptionDriver(**params)
        return (driver,)
