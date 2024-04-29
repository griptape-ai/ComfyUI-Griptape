from griptape.tasks import PromptTask, TextSummaryTask, ToolTask, ToolkitTask
from griptape.structures import Agent
from jinja2 import Template
from .base_task import gtUIBaseTask

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

    CATEGORY = "Griptape/Text"

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

    CATEGORY = "Griptape/Text"

    def encode(self, string_prompt, input_string, clip):
        prompt_text = self.get_prompt_text(string_prompt, input_string)
        tokens = clip.tokenize(prompt_text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]],)
