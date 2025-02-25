from .gtUIWorkflowBase import gtUIWorkflowBase


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


class ContainsAnyDict(dict):
    def __contains__(self, key):
        return True


any = AnyType("*")


class gtUIStartWorkflow(gtUIWorkflowBase):
    DESCRIPTION = "Creates a Griptape Start Workflow Node"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "label": (
                    "STRING",
                    {
                        "default": "Input Label",
                        "tooltip": "This is the label that will be used for the input.",
                    },
                ),
            },
            "optional": {
                "property": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "This is the property that will be used for the input.",
                    },
                )
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT",
            },
        }
        return inputs

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("set_property",)

    CATEGORY = "Griptape/Workflow"

    FUNCTION = "create"

    def create(self, **kwargs):
        unique_id = kwargs.get("unique_id", None)
        prompt = kwargs.get("prompt", None)
        label = kwargs.get("label", None)
        property = kwargs.get("property", None)
        # print(kwargs)
        return (property,)
