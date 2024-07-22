from ..tasks.gtUIBaseTask import gtUIBaseTask


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


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
