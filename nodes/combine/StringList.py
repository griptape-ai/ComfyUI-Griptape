class StringList:
    """
    Griptape Lists of Strings
    """

    DESCRIPTION = "Creates a list of strings"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "input_1": (
                    "STRING",
                    {
                        "tooltip": "A string to add to a list. Connect an input to dynamically create more strings.",
                        "forceInput": True,
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRINGLIST",)
    RETURN_NAMES = ("STRINGLIST",)
    FUNCTION = "create"
    # OUTPUT_IS_LIST = (True,)
    CATEGORY = "Griptape/Text"

    def create(self, **kwargs):
        # Clear the rule_list
        string_list = []

        strings = [value for value in kwargs.values()]
        if len(strings) > 0:
            for string in strings:
                string_list.append(string)
        # rule_list = [rule[0] for rule in [kwargs.values()] if rule is not None]
        return (string_list,)
