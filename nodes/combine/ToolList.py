class ToolList:
    """
    Griptape Tool List
    """

    DESCRIPTION = "Combine tools to give an agent a more complex set of tools."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "tool_1": (
                    "TOOL_LIST",
                    {
                        "tooltip": "A tool to add to the list. Connect an input to dynamically create more tools."
                    },
                ),
            }
        }

    RETURN_TYPES = ("TOOL_LIST",)
    RETURN_NAMES = ("TOOL_LIST",)
    FUNCTION = "create"
    # OUTPUT_IS_LIST = (True,)

    CATEGORY = "Griptape/Agent Tools"

    def create(self, **kwargs):
        tool_list = []

        tools = [value for value in kwargs.values()]
        if len(tools) > 0:
            for tool in tools:
                tool_list.append(tool[0])
        return (tool_list,)
