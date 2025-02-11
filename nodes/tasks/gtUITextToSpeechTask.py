# pyright: reportMissingImports=false
from typing import Any, Tuple

from comfy_execution.graph import ExecutionBlocker
from griptape.artifacts import AudioArtifact, ErrorArtifact
from griptape.drivers.text_to_speech.dummy import DummyTextToSpeechDriver
from griptape.drivers.text_to_speech.elevenlabs import ElevenLabsTextToSpeechDriver
from griptape.structures import Pipeline

# from ..agent.agent import gtComfyAgent as Agent
# from griptape.structures import Agent
from griptape.tasks import TextToSpeechTask

from ...py.griptape_settings import GriptapeSettings
from ..utilities import load_audio_from_artifact
from .gtUIBaseTask import gtUIBaseTask

default_prompt = "{{ input_string }}"


class gtUITextToSpeechTask(gtUIBaseTask):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {"driver": ("TEXT_TO_SPEECH_DRIVER", {"default": None})}
        )
        return inputs

    DESCRIPTION = "Convert a text file to Audio."
    CATEGORY = "Griptape/Audio"

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("AUDIO",)

    def run(self, **kwargs) -> Tuple[Any, ...]:
        # try:
        STRING = kwargs.get("STRING", "")
        input_string = kwargs.get("input_string", "")
        agent = kwargs.get("agent", None)
        driver = kwargs.get("driver", None)
        if not driver:
            settings = GriptapeSettings()
            ELEVEN_LABS_API_KEY = settings.get_settings_key_or_use_env(
                "ELEVEN_LABS_API_KEY"
            )
            if not ELEVEN_LABS_API_KEY:
                ELEVEN_LABS_API_KEY = ""
            driver = agent.drivers_config.text_to_speech_driver
            if isinstance(driver, DummyTextToSpeechDriver):
                driver = ElevenLabsTextToSpeechDriver(
                    api_key=ELEVEN_LABS_API_KEY,
                    model="eleven_multilingual_v2",
                    voice="Matilda",
                )  # type: ignore[reportArgumentType]
        prompt_text = self.get_prompt_text(STRING, input_string)

        task = TextToSpeechTask(
            prompt_text,
            text_to_speech_driver=driver,
        )
        pipeline = Pipeline()
        pipeline.add_task(task)
        result = pipeline.run()

        # Check for output artifact
        artifact = result.output_task.output

        if isinstance(artifact, AudioArtifact):
            audio_output = load_audio_from_artifact(artifact)
        elif isinstance(artifact, ErrorArtifact):
            error_msg = f"Received an error:\n{artifact.value}"
            audio_output = ExecutionBlocker(error_msg)
        else:
            audio_output = ExecutionBlocker("Error: Unexpected artifact type")
        return (audio_output,)
