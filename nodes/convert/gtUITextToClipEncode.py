from ..tasks.gtUIBaseTask import gtUIBaseTask


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


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
