from griptape.artifacts import TextArtifact


class gtUIOutputArtifactNode:
    CATEGORY = "Griptape/Display"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {"INPUT": ("ARTIFACT", {"forceInput": True})},
        }

    RETURN_TYPES = ("ARTIFACT",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "func"
    OUTPUT_NODE = True

    def func(self, INPUT=None):
        if INPUT:
            input_type = type(INPUT)
            if isinstance(INPUT, TextArtifact):
                to_display = f"{repr(INPUT)}"
            else:
                to_display = f"{input_type=}"
            return {
                "ui": {"INPUT": str(to_display)},  # UI message for the frontend
                "result": (INPUT,),
            }
        else:
            return {
                "ui": {"INPUT": ""},
                "result": ("",),
            }
