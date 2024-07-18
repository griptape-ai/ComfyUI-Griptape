from griptape.drivers import OpenAiAudioTranscriptionDriver


class gtUIBaseAudioTranscriptionDriver:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {},
        }

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Drivers/Audio Transcription"

    def create(
        self,
    ):
        driver = OpenAiAudioTranscriptionDriver(model="whisper-1")
        return (driver,)
