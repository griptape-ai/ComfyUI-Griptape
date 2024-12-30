from griptape.tools import (
    WebScraperTool,
)

from .gtUIBaseTool import gtUIBaseTool


class gtUIWebScraper(gtUIBaseTool):
    """
    The Griptape WebScraperTool Tool
    """

    DESCRIPTION = "Scrape the web for information."

    def create(self, **kwargs):
        off_prompt = kwargs.get("off_prompt", False)
        tool = WebScraperTool(
            off_prompt=off_prompt,
        )
        return ([tool],)
