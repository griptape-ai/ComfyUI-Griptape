import os

import folder_paths
from griptape.loaders import PdfLoader, TextLoader


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
        ".md",
        ".pdf",
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
        return {"required": {"text": (sorted(files), {"text_upload": True})}}

    CATEGORY = "Griptape/Text"

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("PATH", "OUTPUT")
    FUNCTION = "gt_load_text"

    def gt_load_text(self, text):
        text_path = folder_paths.get_annotated_filepath(text)
        # get the extension
        ext = os.path.splitext(text_path)[1]
        if ext == ".pdf":
            text_data = PdfLoader().load(text_path)[0]
        else:
            text_data = TextLoader().load(text_path)

        return (
            text_path,
            text_data.value,
        )
        # text_data = ""
        # with open(text_path, "r", encoding="utf-8") as f:
        #     text_data = f.read()
        # return (
        #     text_path,
        #     text_data,
        # )
