from griptape.engines.rag.modules import PromptResponseRagModule

from .gtUIBaseReponseRagModule import gtUIBaseResponseRagModule


class gtUIPromptResponseRagModule(gtUIBaseResponseRagModule):
    """
    Griptape Prompt Response Rag Module.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"] = {
            "prompt_driver": (
                "PROMPT_DRIVER",
                {"tooltip": "Prompt driver to use for the module."},
            ),
            "rulesets": (
                "RULESET",
                {
                    "forceInput": True,
                    "tooltip": "One or more rules to use with RAG.\nUse these to control the RAG response.",
                },
            ),
        }
        return inputs

    def create(self, **kwargs):
        params = {}
        prompt_driver = kwargs.get("prompt_driver", None)
        rulesets = kwargs.get("rulesets", [])
        if prompt_driver:
            params["prompt_driver"] = prompt_driver
        if len(rulesets) > 0:
            params["rulesets"] = rulesets

        module = PromptResponseRagModule(**params)
        return ([module],)
