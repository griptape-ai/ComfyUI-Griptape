import os

from griptape.artifacts import AudioArtifact
from griptape.drivers import DummyTextToSpeechDriver, ElevenLabsTextToSpeechDriver
from griptape.engines import (
    TextToSpeechEngine,
)
from griptape.structures import Pipeline

# from ..agent.agent import gtComfyAgent as Agent
# from griptape.structures import Agent
from griptape.tasks import TextToSpeechTask

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from ..utilities import load_audio_from_artifact
from .gtUIBaseTask import gtUIBaseTask

default_prompt = "{{ input_string }}"
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")


class gtUITextToSpeechTask(gtUIBaseTask):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update({"driver": ("DRIVER", {"default": None})})
        return inputs

    DESCRIPTION = "Convert a text file to Audio."
    CATEGORY = "Griptape/Audio"

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("AUDIO",)

    def run(self, **kwargs):
        try:
            STRING = kwargs.get("STRING", "")
            input_string = kwargs.get("input_string", "")
            agent = kwargs.get("agent", Agent())
            driver = kwargs.get("driver", None)

            if not driver:
                driver = agent.config.text_to_speech_driver
                if isinstance(driver, DummyTextToSpeechDriver):
                    driver = ElevenLabsTextToSpeechDriver(
                        api_key=ELEVEN_LABS_API_KEY,
                        model="eleven_multilingual_v2",
                        voice="Matilda",
                    )
            prompt_text = self.get_prompt_text(STRING, input_string)

            task = TextToSpeechTask(
                prompt_text,
                text_to_speech_engine=TextToSpeechEngine(text_to_speech_driver=driver),
            )
            pipeline = Pipeline()
            pipeline.add_task(task)
            result = pipeline.run()

            # Check for output artifact
            artifact = result.output_task.output

            if isinstance(artifact, AudioArtifact):
                audio_output = load_audio_from_artifact(artifact)

                return (audio_output,)
            else:
                return (str(result.output_task.output.value),)
        except Exception as e:
            print(f"Error in TextToSpeechTask: {str(e)}")
            return (f"Error: {str(e)}",)
