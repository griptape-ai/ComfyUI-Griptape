class gtUIOutputDictionaryNode:
    NAME = "Griptape Display: Dictionary"
    DESCRIPTION = "Display dictionary output."
    CATEGORY = "Griptape/Display"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "INPUT": ("DICT", {"forceInput": True, "multiline": True}),
                "DICTIONARY": ("MARKDOWN", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("DICT",)
    FUNCTION = "func"
    OUTPUT_NODE = True

    def func(self, INPUT=None, DICTIONARY=None):
        if INPUT is not None:
            # Input is connected, use it's value
            return {
                "ui": {"INPUT": str(INPUT)},  # UI message for the frontend
                "result": (str(INPUT),),
            }
        else:
            return {
                "ui": {
                    "DICTIONARY": str(DICTIONARY) if DICTIONARY is not None else "",
                },
                "result": (str(DICTIONARY) if DICTIONARY is not None else "",),
            }
