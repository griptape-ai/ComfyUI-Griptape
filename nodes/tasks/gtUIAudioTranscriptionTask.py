import os
from textwrap import dedent

from griptape.drivers import (
    DummyAudioTranscriptionDriver,
    OpenAiAudioTranscriptionDriver,
)
from griptape.engines import (
    AudioTranscriptionEngine,
)
from griptape.loaders import AudioLoader
from griptape.structures import Pipeline
from griptape.tasks import (
    AudioTranscriptionTask,
)

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseAudioTask import gtUIBaseAudioTask

default_prompt = "{{ input_string }}"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class gtUIAudioTranscriptionTask(gtUIBaseAudioTask):
    DESCRIPTION = "Transcribe an audio file."

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        # Update optional inputs to include 'image' and adjust others as necessary
        inputs["optional"].update(
            {
                "config": ("AGENT",),
                "driver": ("AUDIO_TRANSCRIPTION_DRIVER", {"default": None}),
            }
        )
        return inputs

    CATEGORY = "Griptape/Audio"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)

    def run(self, **kwargs):
        audio = kwargs.get("audio", None)
        audio_filepath = kwargs.get("audio_filepath", None)
        driver = kwargs.get("driver", None)
        agent = kwargs.get("agent", None)
        if not agent:
            agent = Agent()

        audio_artifact = None
        if audio:
            audio = self.save_audio_tempfile(audio)[0]
        elif audio_filepath:
            audio = audio_filepath
        else:
            return ("There is no audio file.",)

        try:
            audio_artifact = AudioLoader().load(audio)
        except Exception as e:
            print(f"Error loading audio file: {e}")
        if audio_artifact:
            if not driver and not agent:
                audio_transcription_driver = OpenAiAudioTranscriptionDriver(
                    model="whisper-1"
                )
            elif not driver and agent:
                audio_transcription_driver = (
                    agent.drivers_config.audio_transcription_driver
                )
            else:
                audio_transcription_driver = driver

            # If the driver is a DummyAudioTranscriptionDriver we'll return a nice error message
            if isinstance(audio_transcription_driver, DummyAudioTranscriptionDriver):
                return (
                    dedent(
                        """
                    I'm sorry, this agent doesn't have access to a valid AudioTranscriptionDriver.
                    You might want to try using a different Agent Configuration.

                    Reach out for help on Discord (https://discord.gg/gnWRz88eym) if you would like some help.
                    """,
                    ),
                )
            engine = AudioTranscriptionEngine(
                audio_transcription_driver=audio_transcription_driver
            )
            # prompt_text = self.get_prompt_text(STRING, input_string)

            task = AudioTranscriptionTask(
                input=lambda _: audio_artifact,
                audio_transcription_engine=engine,
            )

            # if deferred_evaluation:
            #     return ("Audio Transcription Task created", task)
            pipeline = Pipeline()
            pipeline.add_task(task)
            try:
                result = pipeline.run()
            except Exception as e:
                print(e)
            output = result.output_task.output.value
        else:
            output = "No audio provided"
        return (output,)
