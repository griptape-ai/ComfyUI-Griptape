from griptape.drivers.audio_transcription.openai import OpenAiAudioTranscriptionDriver

from .gtUIBaseAudioTranscriptionDriver import gtUIBaseAudioTranscriptionDriver

models = ["whisper-large-v3-turbo", "distil-whisper-large-v3-en", "whisper-large-v3"]
base_url = "https://api.groq.com/openai/v1/"
DEFAULT_MODEL = ""
if len(models) > 0:
    DEFAULT_MODEL = models[0]

DEFAULT_API_KEY = "GROQ_API_KEY"


class gtUIGroqAudioTranscriptionDriver(gtUIBaseAudioTranscriptionDriver):
    DESCRIPTION = "Groq Audio Transcription Driver"

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
        params["base_url"] = base_url
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = OpenAiAudioTranscriptionDriver(**params)
        return (driver,)
