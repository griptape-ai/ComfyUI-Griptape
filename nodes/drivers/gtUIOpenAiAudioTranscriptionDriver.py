from griptape.drivers import OpenAiAudioTranscriptionDriver

from .gtUIBaseAudioTranscriptionDriver import gtUIBaseAudioTranscriptionDriver

openAiAudioTranscriptionModels = ["whisper-1"]

DEFAULT_API_KEY = "OPENAI_API_KEY"


class gtUIOpenAiAudioTranscriptionDriver(gtUIBaseAudioTranscriptionDriver):
    DESCRIPTION = "OpenAI Audio Transcription Driver"

    @classmethod
    def INPUT_TYPES(s):
        models = openAiAudioTranscriptionModels

        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "model": (models, {"default": models[0]}),
            }
        )
        inputs["optional"].update(
            {
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY}),
            }
        )

        return inputs

    RETURN_NAMES = ("DRIVER",)
    RETURN_TYPES = ("DRIVER",)

    def create(self, **kwargs):
        model = kwargs.get("model", openAiAudioTranscriptionModels[0])
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))

        params = {}

        if model:
            params["model"] = model
        if api_key:
            params["api_key"] = api_key
        driver = OpenAiAudioTranscriptionDriver(**params)
        return (driver,)
