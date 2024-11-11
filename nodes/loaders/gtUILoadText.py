import mimetypes
import os

import folder_paths


def is_audio_file(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type is not None and mime_type.startswith("text/")


class gtUILoadText:
    DESCRIPTION = "Load a text file for processing."
    SUPPORTED_FORMATS = (
        ".data",
        ".env",
        ".info",
        ".json",
        ".log",
        ".text",
        ".txt",
        ".yaml",
        ".yml",
        ".csv",
        ".tsv",
    )

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if (
                os.path.isfile(os.path.join(input_dir, f))
                and f.endswith(gtUILoadText.SUPPORTED_FORMATS)
            )
        ]
        return {"required": {"text": (sorted(files), {"text_upload": False})}}

    CATEGORY = "Griptape/Text"

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("PATH", "OUTPUT")
    FUNCTION = "gt_load_text"

    def gt_load_text(self, text):
        text_path = folder_paths.get_annotated_filepath(text)
        text_data = ""
        with open(text_path, "r") as f:
            text_data = f.read()
        return (
            text_path,
            text_data,
        )
