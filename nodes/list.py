class ToolList:
    """
    Griptape Tool List
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "tool_1": ("TOOL",),
                "tool_2": ("TOOL",),
                "tool_3": ("TOOL",),
                "tool_4": ("TOOL",),
                "tool_5": ("TOOL",),
                "tool_6": ("TOOL",),
            }
        }

    RETURN_TYPES = ("TOOL_LIST",)
    RETURN_NAMES = ("tool_list",)
    # OUTPUT_IS_LIST = (True,)
    FUNCTION = "create"

    CATEGORY = "Griptape/Tools"

    def create(
        self,
        tool_1=None,
        tool_2=None,
        tool_3=None,
        tool_4=None,
        tool_5=None,
        tool_6=None,
    ):
        tool_list = [
            tool
            for tool in [tool_1, tool_2, tool_3, tool_4, tool_5, tool_6]
            if tool is not None
        ]
        print(f"{tool_list=}")
        return (tool_list,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
# NODE_CLASS_MAPPINGS = {"DateTime": DateTime}

# A dictionary that contains the friendly/humanly readable titles for the nodes
# NODE_DISPLAY_NAME_MAPPINGS = {"DateTime": "Tool: DateTime"}
