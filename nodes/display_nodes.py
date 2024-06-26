import json
import os
import random

import folder_paths
import numpy as np
from comfy.cli_args import args
from griptape.artifacts import TextArtifact
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from nodes import SaveImage


class gtUIOutputArtifactNode:
    CATEGORY = "Griptape/Display"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {"INPUT": ("ARTIFACT", {"forceInput": True})},
        }

    RETURN_TYPES = ("ARTIFACT",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "func"
    OUTPUT_NODE = True

    def func(self, INPUT=None):
        if INPUT:
            input_type = type(INPUT)
            if isinstance(INPUT, TextArtifact):
                to_display = f"{repr(INPUT)}"
            else:
                to_display = f"{input_type=}"
            return {
                "ui": {"INPUT": str(to_display)},  # UI message for the frontend
                "result": (INPUT,),
            }
        else:
            return {
                "ui": {"INPUT": ""},
                "result": ("",),
            }


class gtUIOutputStringNode:
    NAME = "Griptape Display: Text"
    DESCRIPTION = "Display string output."
    CATEGORY = "Griptape/Display"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}, "optional": {"INPUT": ("STRING", {"forceInput": True})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "func"
    OUTPUT_NODE = True

    def func(self, INPUT=None):
        if INPUT:
            return {
                "ui": {"INPUT": str(INPUT)},  # UI message for the frontend
                "result": (str(INPUT),),
            }
        else:
            return {
                "ui": {"INPUT": ""},
                "result": ("",),
            }


class gtUIOutputDataNode:
    NAME = "Griptape Display: Data"
    DESCRIPTION = "Display output data."
    CATEGORY = "Griptape/Display"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}, "optional": {"INPUT": ("*", {"forceInput": True})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "func"
    OUTPUT_NODE = True

    def func(self, INPUT=None):
        if INPUT:
            return {
                "ui": {"INPUT": str(INPUT)},  # UI message for the frontend
                "result": (str(INPUT),),
            }
        else:
            return {
                "ui": {"INPUT": ""},
                "result": ("",),
            }


# From SaveImage
class gtUISaveImageNode(SaveImage):
    def save_images(
        self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None
    ):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = (
            folder_paths.get_save_image_path(
                filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
            )
        )
        results = list()
        for batch_number, image in enumerate(images):
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            img.save(
                os.path.join(full_output_folder, file),
                pnginfo=metadata,
                compress_level=self.compress_level,
            )
            results.append(
                {"filename": file, "subfolder": subfolder, "type": self.type}
            )
            counter += 1

        return {"ui": {"images": results}, "result": (images,)}


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
