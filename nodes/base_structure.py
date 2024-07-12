from griptape.structures import Structure


class gtUIBaseStructure:
    def __init__(self):
        pass

    DESCRIPTION = "Create a Structure."

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {},
        }

    RETURN_TYPES = ("STRUCTURE",)
    RETURN_NAMES = ("STRUCTURE",)

    FUNCTION = "run"
    # OUTPUT_NODE = True

    CATEGORY = "Griptape/Structure"

    def run(
        self,
    ):
        return (Structure(),)
