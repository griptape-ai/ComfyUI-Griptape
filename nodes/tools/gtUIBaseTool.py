from typing import Any, Tuple

from griptape.tools import BaseTool


class gtUIBaseTool:
    """
    Griptape Base Tool
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "off_prompt": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "label_on": "True (Keep output private)",
                        "label_off": "False (Provide output to LLM)",
                    },
                )
            },
            "optional": {},
            "hidden": {},
        }

    RETURN_TYPES = ("TOOL_LIST",)
    RETURN_NAMES = ("TOOL",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Tools"

    def create(self, **kwargs) -> Tuple[Any, ...]:
        off_prompt = kwargs.get("off_prompt", False)
        return ([BaseTool(off_prompt=off_prompt)],)
