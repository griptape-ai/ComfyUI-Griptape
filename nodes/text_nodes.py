from .base_task import gtUIBaseTask


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class gtUIInputStringNode:
    NAME = "Griptape Create: Text"
    DESCRIPTION = "Create a text string"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "STRING": ("STRING", {"multiline": True, "dynamicPrompts": True})
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Text"

    def run(self, STRING):
        return (STRING,)


class gtUITextToCombo:
    DESCRIPTION = "Convert text to a Combo conditioning"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "STRING": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("combo",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "Griptape/Text"
    FUNCTION = "convert"

    def convert(self, STRING):
        return (STRING,)


class gtUITextToClipEncode(gtUIBaseTask):
    DESCRIPTION = "Convert text to a CLIP conditioning"

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

    CATEGORY = "Griptape/Text"
    FUNCTION = "encode"

    def encode(self, STRING, clip):
        tokens = clip.tokenize(STRING)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]],)


class gtUICLIPTextEncode(gtUIBaseTask):
    DESCRIPTION = "Create a text string and convert it to a CLIP conditioning."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update({"clip": ("CLIP",)})
        del inputs["optional"]["agent"]
        return inputs

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "Griptape/Text"

    def encode(self, STRING, clip, input_string=None):
        prompt_text = self.get_prompt_text(STRING, input_string)
        tokens = clip.tokenize(prompt_text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]],)
