class gtUIOutputStringNode:
    NAME = "Griptape Display: Text"
    DESCRIPTION = "Display string output."
    CATEGORY = "Griptape/Display"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "INPUT": ("STRING", {"forceInput": True}),
                "STRING": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "func"
    OUTPUT_NODE = True

    def func(self, INPUT=None, STRING=None):
        if INPUT is not None:
            # Input is connected, use it's value
            return {
                "ui": {"INPUT": str(INPUT)},  # UI message for the frontend
                "result": (str(INPUT),),
            }
        else:
            return {
                "ui": {
                    "STRING": str(STRING) if STRING is not None else "",
                },
                "result": (str(STRING) if STRING is not None else "",),
            }
