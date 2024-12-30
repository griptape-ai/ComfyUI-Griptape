# pyright: reportMissingImports=false
from io import BytesIO

import numpy as np
import requests
import torch
from PIL import Image


###############################################################################################
#
# Fetch Image From Web
# Based off the work of mnemic-nodes
# https://github.com/MNeMoNiCuZ/ComfyUI-mnemic-nodes/blob/main/nodes/nodes.py
#
###############################################################################################
def pil2tensor(image):
    """Convert a PIL Image to a PyTorch tensor."""
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


class gtUIFetchImage:
    DESCRIPTION = "Fetch an image from a URL."
    OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE", "INT", "INT")  # Image, Width, Height
    RETURN_NAMES = ("IMAGE", "WIDTH", "HEIGHT")
    FUNCTION = "FetchImage"
    CATEGORY = "Griptape/Image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_url": ("STRING", {"multiline": False, "default": ""}),
            },
            "optional": {},
        }

    def FetchImage(self, image_url):
        if not image_url:
            print("Error: No image URL provided.")
            return None, None, None

        # file_extension = os.path.splitext(image_url)[1].lower()
        # if file_extension not in [".jpg", ".jpeg", ".png", ".webp"]:
        #     print(f"Error: Unsupported image format `{file_extension}`")
        #     return None, None, None

        try:
            response = requests.get(image_url)
            if response.status_code != 200:
                print(
                    f"Error: Failed to fetch image from URL with status code {response.status_code}"
                )
                return None, None, None

            image = Image.open(BytesIO(response.content)).convert("RGB")
            width, height = image.size

            image_tensor = pil2tensor(image)

        except Exception as e:
            print(f"Error processing the image: {e}")
            return None, None, None

        return image_tensor, width, height
