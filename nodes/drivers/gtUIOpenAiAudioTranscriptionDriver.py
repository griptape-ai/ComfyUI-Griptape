from griptape.drivers import OpenAiAudioTranscriptionDriver

from .gtUIBaseAudioTranscriptionDriver import gtUIBaseAudioTranscriptionDriver

models = ["whisper-1"]

DEFAULT_API_KEY = "OPENAI_API_KEY"


class gtUIOpenAiAudioTranscriptionDriver(gtUIBaseAudioTranscriptionDriver):
    DESCRIPTION = "OpenAI Audio Transcription Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "audio_transcription_model": (
                    models,
                    {
                        "default": models[0],
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
        model = kwargs.get("audio_transcription_model", models[0])
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
