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
        inputs = super().INPUT_TYPES()
        inputs["optional"].update({"clip": ("CLIP",)})
        del inputs["optional"]["agent"]
        return inputs

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "Griptape/Create"

    def encode(self, string_prompt, clip, input_string=None):
        prompt_text = self.get_prompt_text(string_prompt, input_string)
        tokens = clip.tokenize(prompt_text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]],)
