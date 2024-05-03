from .base_task import gtUIBaseTask

import torch
import base64
from PIL import Image
import numpy as np
from io import BytesIO


class gtUIBaseImageTask(gtUIBaseTask):
    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        # Update optional inputs to include 'image' and adjust others as necessary
        inputs["required"].update(
            {
                "image": ("IMAGE",),
            }
        )
        return inputs

    CATEGORY = "Griptape/Create"

    def run(self, string_prompt, image, input_string=None, agent=None):
        output = "Output"
        return (output, agent)
