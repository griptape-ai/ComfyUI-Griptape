from griptape.tasks import PromptTask, TextSummaryTask, ToolTask, ToolkitTask
from griptape.structures import Agent
from jinja2 import Template
from .base_task import gtUIBaseTask
import torch
import numpy as np
import os
import requests
from PIL import Image
from io import BytesIO


default_prompt = "{{ input_string }}"


class gtUIInputStringNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {"STRING": ("STRING", {"multiline": True})},
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Create"

    def run(self, STRING):
        return (STRING,)


class gtUICLIPTextEncode(gtUIBaseTask):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        # "dynamicPrompts": True,
                        "default": default_prompt,
                    },
                ),
                "clip": ("CLIP",),
            },
            "optional": {"input_string": ("STRING", {"forceInput": True})},
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "Griptape/Create"

    def encode(self, string_prompt, input_string, clip):
        prompt_text = self.get_prompt_text(string_prompt, input_string)
        tokens = clip.tokenize(prompt_text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]],)


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
    OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE", "INT", "INT")  # Image, Width, Height
    RETURN_NAMES = ("image", "width", "height")
    FUNCTION = "FetchImage"
    CATEGORY = "Griptape/Create"

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
