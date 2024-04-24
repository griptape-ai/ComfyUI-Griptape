from griptape.tools import DateTime, Calculator, WebScraper, BaseTool, FileManager
from griptape.loaders import WebLoader
from griptape.drivers import MarkdownifyWebScraperDriver

from .base_tool import gtUIBaseTool
import folder_paths
import os


class gtUIFileManager(gtUIBaseTool):
    """
    The Griptape File Manager Tool
    """

    @classmethod
    def INPUT_TYPES(s):
        workdir = os.getenv("HOME")
        return {
            "required": {"off_prompt": ("BOOLEAN", {"default": True})},
            "optional": {"workdir": ("STRING", {"default": f"{workdir}"})},
        }

    def create(self, off_prompt, workdir=""):
        tool = FileManager(off_prompt=off_prompt, workdir=workdir)
        return (tool,)


class gtUICalculator(gtUIBaseTool):
    """
    The Griptape Calculator Tool
    """

    def create(self, off_prompt):
        tool = Calculator(off_prompt=off_prompt)
        return (tool,)


class gtUIWebScraper(gtUIBaseTool):
    """
    The Griptape WebScraper Tool
    """

    def create(self, off_prompt):
        tool = WebScraper(
            off_prompt=off_prompt,
            web_loader=WebLoader(
                web_scraper_driver=MarkdownifyWebScraperDriver(timeout=1000)
            ),
        )
        return (tool,)


class gtUIDateTime(gtUIBaseTool):
    """
    The Griptape DateTime Tool
    """

    def create(self, off_prompt):
        tool = DateTime(off_prompt=off_prompt)
        return (tool,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
# NODE_CLASS_MAPPINGS = {"DateTime": DateTime}

# A dictionary that contains the friendly/humanly readable titles for the nodes
# NODE_DISPLAY_NAME_MAPPINGS = {"DateTime": "Tool: DateTime"}
