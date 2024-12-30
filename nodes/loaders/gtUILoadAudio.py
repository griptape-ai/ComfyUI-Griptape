# pyright: reportMissingImports=false

import mimetypes
import os

import folder_paths
import torchaudio


def is_audio_file(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type is not None and mime_type.startswith("audio/")


class gtUILoadAudio:
    DESCRIPTION = "Load an audio file for processing."
    SUPPORTED_FORMATS = (".wav", ".mp3", ".ogg", ".flac", ".aiff", ".aif")

    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if (
                os.path.isfile(os.path.join(input_dir, f))
                and f.endswith(gtUILoadAudio.SUPPORTED_FORMATS)
            )
        ]
        return {"required": {"audio": (sorted(files), {"audio_upload": False})}}

    CATEGORY = "Griptape/Audio"

    RETURN_TYPES = ("STRING", "AUDIO")
    RETURN_NAMES = ("AUDIO_PATH", "AUDIO")
    FUNCTION = "gt_load_audio"

    def gt_load_audio(self, audio):
        audio_path = folder_paths.get_annotated_filepath(audio)
        waveform, sample_rate = torchaudio.load(audio_path)
        audio = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        return (
            audio_path,
            audio,
        )
