from griptape.drivers import ElevenLabsTextToSpeechDriver
from griptape.tools.text_to_speech.tool import TextToSpeechTool

from ...py.griptape_settings import GriptapeSettings
from .gtUIBaseTool import gtUIBaseTool


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
            "required": {
                "off_prompt": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "label_on": "True (Keep output private)",
                        "label_off": "False (Provide output to LLM)",
                    },
                )
            },
            "optional": {"driver": ("TEXT_TO_SPEECH_DRIVER", {"default": None})},
        }

    def create(self, off_prompt, driver=None):
        if not driver:
            settings = GriptapeSettings()
            api_key = settings.get_settings_key_or_use_env("ELEVEN_LABS_API_KEY")

            driver = ElevenLabsTextToSpeechDriver(
                api_key=api_key, model="eleven_multilingual_v2", voice="Matilda"
            )

        tool = TextToSpeechTool(
            off_prompt=off_prompt,
            text_to_speech_driver=driver,
        )

        return ([tool],)
