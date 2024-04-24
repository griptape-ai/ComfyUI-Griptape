from griptape.tasks import PromptTask, TextSummaryTask, ToolTask, ToolkitTask
from griptape.structures import Agent
from jinja2 import Template

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
