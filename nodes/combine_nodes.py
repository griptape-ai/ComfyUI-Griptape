class ConcatenateStrings:
    """
    Concatenate Strings
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "string_1": ("STRING", {"forceInput": True}),
                "string_2": ("STRING", {"forceInput": True}),
                "string_3": ("STRING", {"forceInput": True}),
                "string_4": ("STRING", {"forceInput": True}),
                "separator": ("STRING", {"default": "\\n"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Combine-Expand"

    def create(
        self,
        string_1="",
        string_2="",
        string_3="",
        string_4="",
        separator="\n",
    ):
        # If the user enters \n, we need to convert it to a newline
        separator = separator.replace("\\n", "\n")

        # Join strings by newline
        concatenated_string = separator.join(
            [
                string
                for string in [string_1, string_2, string_3, string_4]
                if not string == ""
            ],
        )

        return (concatenated_string,)


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
                "tool_2": ("TOOL",),
                "tool_3": ("TOOL",),
                "tool_4": ("TOOL",),
                "tool_5": ("TOOL",),
                "tool_6": ("TOOL",),
                "tool_1": ("TOOL",),
            }
        }

    RETURN_TYPES = ("TOOL_LIST",)
    RETURN_NAMES = ("TOOL_LIST",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Combine-Expand"

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
        return (tool_list,)
