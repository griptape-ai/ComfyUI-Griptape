from griptape.tools import (
    DateTime,
)

from .gtUIBaseTool import gtUIBaseTool


class gtUIDateTime(gtUIBaseTool):
    """
    The Griptape DateTime Tool
    """

    DESCRIPTION = "Get the current date and time."

    def create(self, off_prompt):
        tool = DateTime(off_prompt=off_prompt)
        return ([tool],)
