from griptape.tools import (
    WebScraper,
)

from .gtUIBaseTool import gtUIBaseTool


class gtUIWebScraper(gtUIBaseTool):
    """
    The Griptape WebScraper Tool
    """

    DESCRIPTION = "Scrape the web for information."

    def create(self, off_prompt):
        tool = WebScraper(
            off_prompt=off_prompt,
        )
        return ([tool],)
