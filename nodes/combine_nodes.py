class MergeTexts:
    """
    Merge Texts
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "input_1": ("STRING", {"forceInput": True}),
                "input_2": ("STRING", {"forceInput": True}),
                "input_3": ("STRING", {"forceInput": True}),
                "input_4": ("STRING", {"forceInput": True}),
                "input_5": ("STRING", {"forceInput": True}),
                "input_6": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Text"

    def create(
        self,
        input_1="",
        input_2="",
        input_3="",
        input_4="",
        input_5="",
        input_6="",
    ):
        # Join strings by newline
        concatenated_string = "\n\n".join(
            [
                string
                for string in [input_1, input_2, input_3, input_4, input_5, input_6]
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
                "tool_1": ("TOOL_LIST",),
                "tool_2": ("TOOL_LIST",),
                "tool_3": ("TOOL_LIST",),
                "tool_4": ("TOOL_LIST",),
                "tool_5": ("TOOL_LIST",),
                "tool_6": ("TOOL_LIST",),
            }
        }

    RETURN_TYPES = ("TOOL_LIST",)
    RETURN_NAMES = ("TOOL_LIST",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Tools"

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
            tool[0]
            for tool in [
                tool_1,
                tool_2,
                tool_3,
                tool_4,
                tool_5,
                tool_6,
            ]
            if tool is not None
        ]
        return (tool_list,)
