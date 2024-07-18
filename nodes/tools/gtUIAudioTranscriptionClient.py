from griptape.drivers import OpenAiAudioTranscriptionDriver
from griptape.engines import AudioTranscriptionEngine
from griptape.tools.audio_transcription_client.tool import AudioTranscriptionClient

from .gtUIBaseTool import gtUIBaseTool


class gtUIAudioTranscriptionClient(gtUIBaseTool):
    """
    Griptape AudioTranscriptionClient Tool
    """

    DESCRIPTION = "Transcribe audio to text"

    @classmethod
    def INPUT_TYPES(s):
        # inputs = super().INPUT_TYPES()
        # inputs["optional"].update({"driver": ("DRIVER",)})
        # return inputs

        return {
            "required": {"off_prompt": ("BOOLEAN", {"default": True})},
            "optional": {"driver": ("DRIVER", {"default": None})},
        }

    def create(self, off_prompt, driver=None):
        if not driver:
            driver = OpenAiAudioTranscriptionDriver(model="whisper-1")

        tool = AudioTranscriptionClient(
            off_prompt=off_prompt,
            engine=AudioTranscriptionEngine(
                audio_transcription_driver=driver,
            ),
        )

        return ([tool],)
