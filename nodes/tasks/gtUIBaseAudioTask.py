# pyright: reportMissingImports=false
import io
import tempfile
from typing import Any, Tuple

import torchaudio
from griptape.drivers import OpenAiAudioTranscriptionDriver

from .gtUIBaseTask import gtUIBaseTask


class gtUIBaseAudioTask(gtUIBaseTask):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "audio_filepath": (
                    "STRING",
                    {
                        "forceInput": True,
                    },
                ),
                "audio": ("AUDIO", {}),
                "driver": ("DRIVER", {}),
            },
        )
        # inputs["optional"].update({"driver": ("DRIVER",)})
        del inputs["optional"]["input_string"]
        del inputs["optional"]["agent"]
        del inputs["required"]["STRING"]
        return inputs

    CATEGORY = "Griptape/Audio"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)

    def save_audio_tempfile(self, audio_data):
        temp_files = []

        for waveform in audio_data["waveform"]:
            with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as temp_file:
                temp_filename = temp_file.name

                # Save the audio to the buffer
                buff = io.BytesIO()
                torchaudio.save(
                    buff, waveform, audio_data["sample_rate"], format="FLAC"
                )

                # Write the buffer's contents to the temporary file
                with open(temp_filename, "wb") as f:
                    f.write(buff.getbuffer())

                temp_files.append(temp_filename)

        return temp_files

    def run(self, **kwargs) -> Tuple[Any, ...]:
        driver = kwargs.get("driver", None)

        if not driver:
            driver = OpenAiAudioTranscriptionDriver(model="whisper-1")
        output = "Output"
        return (output,)
