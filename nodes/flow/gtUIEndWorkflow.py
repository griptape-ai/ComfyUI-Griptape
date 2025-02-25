class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class gtUIEndWorkflow:
    """
    Takes any inputs
    """

    DESCRIPTION = "Creates a Griptape End Workflow Node"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "OUTPUT_1": (
                    any,
                    {
                        "tooltip": "An input to display. Connect an input to dynamically create more inputs."
                    },
                ),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "create"

    OUTPUT_NODE = True
    CATEGORY = "Griptape/Workflow"

    def create(
        self,
        **kwargs,
    ):
        # all the outputs are in the kwargs as OUTPUT_1, OUTPUT_2, etc.

        print(kwargs)

        return ()
