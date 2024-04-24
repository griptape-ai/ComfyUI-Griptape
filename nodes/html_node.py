class HtmlNode:
    CATEGORY = "Griptape/Output"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"INPUT": ("STRING", {"default": "input"})}}

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "func"

    def func(self):
        return ()
