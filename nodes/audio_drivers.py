from griptape.drivers import OpenAiAudioTranscriptionDriver

from .base_driver import gtUIBaseAudioTranscriptionDriver

openAiAudioTranscriptionModels = ["whisper-1"]


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
        return inputs

    RETURN_NAMES = ("DRIVER",)
    RETURN_TYPES = ("DRIVER",)

    def create(
        self,
        model,
    ):
        driver = OpenAiAudioTranscriptionDriver(model=model)
        return (driver,)
