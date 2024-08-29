from griptape.tools import (
    DateTimeTool,
)

from .gtUIBaseTool import gtUIBaseTool


class gtUIDateTime(gtUIBaseTool):
    """
    The Griptape DateTimeTool Tool
    """

    DESCRIPTION = "Get the current date and time."

    def create(self, off_prompt):
        tool = DateTimeTool(off_prompt=off_prompt)
        return ([tool],)
