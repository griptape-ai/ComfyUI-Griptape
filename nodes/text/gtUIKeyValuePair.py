class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class gtUIKeyValuePair:
    NAME = "Griptape Create: Key Value Pair"
    DESCRIPTION = "Create a Key Value Pair"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "key": ("STRING", {"multiline": False, "dynamicPrompts": False}),
                "value": ("STRING", {"multiline": True, "dynamicPrompts": False}),
            },
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("DICT",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Text"

    def create(self, **kwargs):
        key = kwargs.get("key", "")
        value = kwargs.get("value", "")

        return ({key: value},)
