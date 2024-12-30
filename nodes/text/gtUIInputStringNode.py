class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class gtUIInputStringNode:
    NAME = "Griptape Create: Text"
    DESCRIPTION = "Create a text string"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "STRING": ("STRING", {"multiline": True, "dynamicPrompts": False})
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Text"

    def run(self, STRING):
        return (STRING,)
