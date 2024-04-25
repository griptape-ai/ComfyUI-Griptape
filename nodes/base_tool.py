from griptape.tools import DateTime, Calculator, WebScraper, BaseTool, FileManager
from griptape.loaders import WebLoader
from griptape.drivers import MarkdownifyWebScraperDriver


class gtUIBaseTool:
    """
    Griptape Base Tool
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"off_prompt": ("BOOLEAN", {"default": True})}}

    RETURN_TYPES = ("TOOL",)
    RETURN_NAMES = ("tool",)
    FUNCTION = "create"

    CATEGORY = "Griptape/Tools"

    def create(self, off_prompt):
        return (BaseTool(off_prompt=off_prompt),)
