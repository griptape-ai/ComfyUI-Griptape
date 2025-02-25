class gtUIWorkflowBase:
    DESCRIPTION = "Creates a base Griptape Start Workflow "

    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {},
            "optional": {
                "label": (
                    "STRING",
                    {
                        "default": "Input Label",
                        "tooltip": "This is the label that will be used for the input.",
                    },
                ),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT",
            },
        }
        return inputs

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    CATEGORY = "Griptape/Workflow"

    FUNCTION = "create"

    def create(run, **kwargs):
        unique_id = kwargs.get("unique_id", None)
        prompt = kwargs.get("prompt", None)
        label = kwargs.get("label", None)
        return ()
