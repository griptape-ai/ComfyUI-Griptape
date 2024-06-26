import os

import folder_paths


class gtUILoadAudio:
    DESCRIPTION = "Load an audio file for processing."

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
        ]
        return {
            "required": {"audio": (sorted(files), {"audio_upload": True})},
        }

    CATEGORY = "Griptape/Audio"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("AUDIO PATH",)
    FUNCTION = "load_audio"

    def load_audio(self, audio):
        audio_path = folder_paths.get_annotated_filepath(audio)

        return (audio_path,)
