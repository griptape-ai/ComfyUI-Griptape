class gtUIMergeInputs:
    """
    Takes any inputs and merges them.. like strings, but just any inputs instead.
    """

    DESCRIPTION = "Merge multiple inputs into one."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "input_1": (
                    "*",
                    {
                        "tooltip": "An input to merge. Connect an input to dynamically create more inputs."
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Text"

    def create(
        self,
        **kwargs,
    ):
        concatenated_value = ""
        inputs = [value for value in kwargs.values()]
        for input in inputs:
            concatenated_value += "\n\n" + str(input)
        return (concatenated_value,)
