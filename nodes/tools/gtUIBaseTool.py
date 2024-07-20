from griptape.tools import BaseTool


class gtUIBaseTool:
    """
    Griptape Base Tool
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"off_prompt": ("BOOLEAN", {"default": False})},
            "optional": {},
            "hidden": {},
        }

    RETURN_TYPES = ("TOOL_LIST",)
    RETURN_NAMES = ("TOOL",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Tools"

    def create(self, off_prompt):
        return ([BaseTool(off_prompt=off_prompt)],)
