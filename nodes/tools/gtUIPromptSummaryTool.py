from griptape.engines import PromptSummaryEngine
from griptape.tools import PromptSummaryTool

from .gtUIBaseTool import gtUIBaseTool


class gtUIPromptSummaryTool(gtUIBaseTool):
    """
    The Griptape Prompt Summary Tool
    """

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "prompt_driver": ("PROMPT_DRIVER", {}),
            }
        )
        del inputs["required"]["off_prompt"]

        return inputs

    DESCRIPTION = (
        "Prompt Summary Tool - Summarizes information that is found in Task Memory."
    )

    def create(self, **kwargs):
        prompt_driver = kwargs.get("prompt_driver", None)

        params = {}
        engine = PromptSummaryEngine(prompt_driver=prompt_driver)
        params["prompt_summary_engine"] = engine
        tool = PromptSummaryTool(**params)
        return ([tool],)
