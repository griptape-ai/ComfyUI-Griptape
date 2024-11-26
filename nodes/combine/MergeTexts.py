class MergeTexts:
    """
    Merge Texts
    """

    DESCRIPTION = "Merge multiple strings into one."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "merge_string": ("STRING", {"default": "\\n\\n"}),
                "input_1": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "forceInput": True,
                        "tooltip": "A text input to merge. Connect an input to dynamically create more inputs.",
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
        merged_text = ""

        sep = kwargs["merge_string"].replace("\\n", "\n")
        del kwargs["merge_string"]

        inputs = [value for value in kwargs.values()]

        merged_text = sep.join(inputs)
        return (merged_text.strip(),)
