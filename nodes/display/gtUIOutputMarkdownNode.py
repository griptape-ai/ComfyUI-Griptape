from .gtUIOutputStringNode import gtUIOutputStringNode


class gtUIOutputMarkdownNode(gtUIOutputStringNode):
    NAME = "Griptape Display: Text as Markdown"
    DESCRIPTION = "Display string output as Markdown"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["optional"]["STRING"] = ("MARKDOWN", {"multiline": True})
        return inputs
