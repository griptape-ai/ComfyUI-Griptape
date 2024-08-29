from griptape.drivers import DuckDuckGoWebSearchDriver
from griptape.tools import (
    WebSearchTool,
)

from .gtUIBaseTool import gtUIBaseTool


class gtUIWebSearch(gtUIBaseTool):
    """
    The Griptape Web Search Tool
    """

    DESCRIPTION = "Search the web."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "driver": ("WEB_SEARCH_DRIVER", {"default": None}),
            }
        )
        return inputs

    def create(self, off_prompt, driver=None):
        if not driver:
            driver = DuckDuckGoWebSearchDriver()
        tool = WebSearchTool(
            web_search_driver=driver,
            off_prompt=off_prompt,
        )
        return ([tool],)
