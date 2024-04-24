class JoinStringListNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "texts": ("STRING", {"forceInput": True}),
                "separator": ("STRING", {"default": "/"}),
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "perform_join_string_list"
    CATEGORY = "text utility"

    def perform_join_string_list(self, texts, separator):
        return (separator[0].join(texts),)
