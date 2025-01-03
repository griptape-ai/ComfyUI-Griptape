class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class gtUISwitchNode:
    """
    Takes any inputs and gives the user the ability to choose which one will be the output.
    """

    DESCRIPTION = "Merge multiple inputs into one."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "input_1": (
                    any,
                    {
                        "tooltip": "An input to choose. Connect an input to dynamically create more inputs."
                    },
                ),
                "switch": (
                    "INT",
                    {
                        "default": 1,
                        "tooltip": "The input to choose.",
                    },
                ),
            },
        }

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Agent Utils"

    def create(
        self,
        **kwargs,
    ):
        switch = kwargs.pop("switch")
        inputs = [value for value in kwargs.values()]
        output = inputs[switch - 1]
        return (output,)
