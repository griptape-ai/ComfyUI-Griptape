from griptape.tools import (
    FileManagerTool,
)

from .gtUIBaseTool import gtUIBaseTool


class gtUIFileManager(gtUIBaseTool):
    """
    The Griptape File Manager Tool
    """

    DESCRIPTION = "Access files on disk."

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"off_prompt": ("BOOLEAN", {"default": True})},
        }

    def create(self, off_prompt, workdir=""):
        tool = FileManagerTool(off_prompt=off_prompt)
        return ([tool],)
