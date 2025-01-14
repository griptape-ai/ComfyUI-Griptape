from griptape.drivers import GooglePromptDriver
from griptape.tools import QueryTool

from ..patches.gemini_query_tool import GeminiQueryTool
from .gtUIBaseTool import gtUIBaseTool


class gtUIQueryTool(gtUIBaseTool):
    """
    The Griptape Query Tool
    """

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "prompt_driver": ("PROMPT_DRIVER", {}),
            }
        )
        del inputs["required"]["off_prompt"]

        return inputs

    DESCRIPTION = "Query Tool - allows the agent to query other tool output."

    def create(self, **kwargs):
        prompt_driver = kwargs.get("prompt_driver", None)

        params = {}
        if prompt_driver:
            params["prompt_driver"] = prompt_driver
        if isinstance(prompt_driver, GooglePromptDriver):
            tool = GeminiQueryTool()
        else:
            tool = QueryTool(**params)
        return ([tool],)
