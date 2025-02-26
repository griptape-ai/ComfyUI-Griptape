class MergeDictionary:
    """
    Create Context
    """

    DESCRIPTION = "Merge Multiple Key Value Pairs into a Dictionary"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "dict_1": (
                    "DICT",
                    {
                        "multiline": False,
                        "forceInput": True,
                        "tooltip": "A Key Value DICT. Connect a DICT to dynamically create more inputs.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("DICT",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Text"

    def create(
        self,
        **kwargs,
    ):
        merged_dict = {}

        dicts = [value for value in kwargs.values()]
        # Extract the single key-value pair from each dictionary and combine them
        merged_dict = {list(item.keys())[0]: list(item.values())[0] for item in dicts}

        return (merged_dict,)
