import random

import folder_paths

from .SaveImageNode import gtUISaveImageNode


# From PreviewImage
class gtUIOutputImageNode(gtUISaveImageNode):
    DESCRIPTION = "Display image output."

    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + "".join(
            random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5)
        )
        self.compress_level = 1

    CATEGORY = "Griptape/Display"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {"images": ("IMAGE", {"forceInput": True})},
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("OUTPUT",)
    OUTPUT_NODE = True
