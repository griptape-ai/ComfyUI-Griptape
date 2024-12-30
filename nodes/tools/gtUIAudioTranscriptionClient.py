from typing import Any, Tuple

from griptape.drivers import OpenAiAudioTranscriptionDriver
from griptape.tools.audio_transcription.tool import AudioTranscriptionTool

from .gtUIBaseTool import gtUIBaseTool


class gtUIAudioTranscriptionClient(gtUIBaseTool):
    """
    Griptape AudioTranscriptionClient Tool
    """

    DESCRIPTION = "Transcribe audio to text"

    @classmethod
    def INPUT_TYPES(cls):
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
            "optional": {"driver": ("DRIVER", {"default": None})},
        }

    def create(self, **kwargs) -> Tuple[Any, ...]:
        off_prompt = kwargs.get("off_prompt", True)
        driver = kwargs.get("driver", None)

        if not driver:
            driver = OpenAiAudioTranscriptionDriver(model="whisper-1")
        params = {}
        if driver:
            params["audio_transcription_driver"] = driver
        params["off_prompt"] = off_prompt
        tool = AudioTranscriptionTool(**params)

        return ([tool],)
