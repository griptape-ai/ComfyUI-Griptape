class gtUIOutputDataNode:
    NAME = "Griptape Display: Data"
    DESCRIPTION = "Display output data."
    CATEGORY = "Griptape/Display"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}, "optional": {"INPUT": ("*", {"forceInput": True})}}

    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        return True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "func"
    OUTPUT_NODE = True

    def func(self, INPUT=None):
        if INPUT:
            return {
                "ui": {"INPUT": str(INPUT)},  # UI message for the frontend
                "result": (str(INPUT),),
            }
        else:
            return {
                "ui": {"INPUT": ""},
                "result": ("",),
            }
