from griptape.drivers import OpenAiChatPromptDriver
from griptape.engines.rag.modules import TranslateQueryRagModule

from .gtUIBaseQueryRagModule import gtUIBaseQueryRagModule


class gtUITranslateQueryRagModule(gtUIBaseQueryRagModule):
    """
    Griptape Translate Query Rag Module. Used for the Query Stage of the RAG Engine.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"] = {
            "language": (
                "STRING",
                {
                    "default": "english",
                    "tooltip": "Language to translate the query to.",
                },
            ),
            "prompt_driver": (
                "PROMPT_DRIVER",
                {"tooltip": "Prompt driver to use for the module."},
            ),
        }
        return inputs

    def create(self, **kwargs):
        prompt_driver = kwargs.get("prompt_driver", None)
        if not prompt_driver:
            prompt_driver = OpenAiChatPromptDriver(model="gpt-4o")

        params = {}
        params["language"] = kwargs.get("language", "english")
        params["prompt_driver"] = prompt_driver
        module = TranslateQueryRagModule(**params)
        return ([module],)
