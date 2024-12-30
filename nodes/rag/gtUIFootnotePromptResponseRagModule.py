from griptape.engines.rag.modules import FootnotePromptResponseRagModule

from .gtUIPromptResponseRagModule import gtUIPromptResponseRagModule


class gtUIFootnotePromptResponseRagModule(gtUIPromptResponseRagModule):
    """
    Griptape Footnote Prompt Response Rag Module.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        return inputs

    def create(self, **kwargs):
        params = {}
        prompt_driver = kwargs.get("prompt_driver", None)
        rulesets = kwargs.get("rulesets", [])
        if prompt_driver:
            params["prompt_driver"] = prompt_driver
        if len(rulesets) > 0:
            params["rulesets"] = rulesets

        module = FootnotePromptResponseRagModule(**params)
        return ([module],)
