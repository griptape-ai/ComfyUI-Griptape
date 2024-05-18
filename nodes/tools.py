import os

from griptape.drivers import MarkdownifyWebScraperDriver
from griptape.loaders import WebLoader
from griptape.tools import Calculator, DateTime, FileManager, WebScraper

from .base_tool import gtUIBaseTool


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
