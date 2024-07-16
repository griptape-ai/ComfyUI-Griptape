import os

from griptape.drivers import ElevenLabsTextToSpeechDriver
from griptape.engines import TextToSpeechEngine
from griptape.tools.text_to_speech_client.tool import TextToSpeechClient

from .BaseTool import gtUIBaseTool


class gtUITextToSpeechClient(gtUIBaseTool):
    """
    Griptape TextToSpeech Tool
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
            api_key = os.getenv("ELEVEN_LABS_API_KEY")

            driver = ElevenLabsTextToSpeechDriver(
                api_key=api_key, model="eleven_multilingual_v2", voice="Matilda"
            )

        tool = TextToSpeechClient(
            off_prompt=off_prompt,
            engine=TextToSpeechEngine(
                text_to_speech_driver=driver,
            ),
        )

        return ([tool],)
