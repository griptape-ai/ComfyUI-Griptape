from .base_task import gtUIBaseTask


class gtUIInputStringNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {"STRING": ("STRING", {"multiline": True})},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Create"

    def run(self, STRING):
        return (STRING,)


class gtUITextToClipEncode(gtUIBaseTask):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "STRING": ("STRING", {"forceInput": True}),
                "clip": ("CLIP",),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Utilities"
    FUNCTION = "encode"

    def encode(self, string, clip):
        tokens = clip.tokenize(string)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]],)


class gtUICLIPTextEncode(gtUIBaseTask):
    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update({"clip": ("CLIP",)})
        del inputs["optional"]["agent"]
        return inputs

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "Griptape/Create"

    def encode(self, STRING, clip, input_string=None):
        prompt_text = self.get_prompt_text(STRING, input_string)
        tokens = clip.tokenize(prompt_text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]],)
