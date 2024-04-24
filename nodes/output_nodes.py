from nodes import SaveImage, PreviewImage
import folder_paths
import random
import json
import os

from PIL import Image, ImageOps, ImageSequence
from comfy.cli_args import args
from PIL.PngImagePlugin import PngInfo
import numpy as np


class gtUIOutputStringNode:
    CATEGORY = "Griptape/Preview"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}, "optional": {"INPUT": ("STRING", {"forceInput": True})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "func"
    OUTPUT_NODE = True

    def func(self, INPUT):

        return {
            "ui": {"INPUT": INPUT},  # UI message for the frontend
            "result": (INPUT,),
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
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + "".join(
            random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5)
        )
        self.compress_level = 1

    CATEGORY = "Griptape/Images"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {"images": ("IMAGE", {"forceInput": True})},
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("OUTPUT",)
    # FUNCTION = "func"
    OUTPUT_NODE = True

    # def func(self, INPUT, filename_prefix="gtUI", prompt=None):

    #     return {
    #         "ui": {"INPUT": INPUT},  # UI message for the frontend
    #         "result": (INPUT,),
    #     }
