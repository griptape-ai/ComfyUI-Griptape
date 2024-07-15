from griptape.tools import (
    Calculator,
)

from .BaseTool import gtUIBaseTool


class gtUICalculator(gtUIBaseTool):
    """
    The Griptape Calculator Tool
    """

    DESCRIPTION = "Perform calculations."

    def create(self, off_prompt):
        tool = Calculator(off_prompt=off_prompt)
        return ([tool],)
