from griptape.tools import CalculatorTool

from .gtUIBaseTool import gtUIBaseTool


class gtUICalculator(gtUIBaseTool):
    """
    The Griptape Calculator Tool
    """

    DESCRIPTION = "Perform calculations."

    def create(self, **kwargs):
        off_prompt = kwargs.get("off_prompt", False)
        tool = CalculatorTool(off_prompt=off_prompt)
        return ([tool],)
