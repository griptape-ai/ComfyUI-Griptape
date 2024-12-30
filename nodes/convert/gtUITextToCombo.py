class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class gtUITextToCombo:
    DESCRIPTION = "Convert text to a Combo conditioning"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "STRING": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("combo",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Text"
    FUNCTION = "convert"

    def convert(self, STRING):
        return (STRING,)
