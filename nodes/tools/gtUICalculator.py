from griptape.tools import CalculatorTool

from .gtUIBaseTool import gtUIBaseTool


class gtUICalculator(gtUIBaseTool):
    """
    The Griptape Calculator Tool
    """

    DESCRIPTION = "Perform calculations."

    def create(self, off_prompt):
        tool = CalculatorTool(off_prompt=off_prompt)
        return ([tool],)
