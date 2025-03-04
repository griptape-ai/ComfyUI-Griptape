class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class StringList:
    """
    Griptape Lists of Strings
    """

    DESCRIPTION = "Creates a list of strings"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "input_1": (
                    any,
                    {
                        "tooltip": "A string to add to a list. Connect an input to dynamically create more strings.",
                        "forceInput": True,
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING_LIST",)
    RETURN_NAMES = ("STRING_LIST",)
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
