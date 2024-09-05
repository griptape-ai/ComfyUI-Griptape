class gtUIModuleList:
    """
    Griptape Module List
    """

    DESCRIPTION = "Combine rag modules into a list to be used with RAG Engines."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "module_1": (
                    "MODULE_LIST",
                    {
                        "tooltip": "A module to add to the list. Connect an input to dynamically create more inputs."
                    },
                ),
            }
        }

    RETURN_TYPES = ("MODULE_LIST",)
    RETURN_NAMES = ("MODULE_LIST",)
    FUNCTION = "create"
    # OUTPUT_IS_LIST = (True,)

    CATEGORY = "Griptape/RAG"

    def create(self, **kwargs):
        module_list = []

        modules = [value for value in kwargs.values()]
        if len(modules) > 0:
            for module in modules:
                module_list.append(module[0])
        return (module_list,)
