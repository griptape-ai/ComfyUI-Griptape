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
    def INPUT_TYPES(cls):
        return {
            "required": {
                "off_prompt": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "label_on": "True (Keep output private)",
                        "label_off": "False (Provide output to LLM)",
                    },
                )
            },
        }

    def create(self, **kwargs):
        off_prompt = kwargs.get("off_prompt", True)
        tool = FileManagerTool(off_prompt=off_prompt)
        return ([tool],)
