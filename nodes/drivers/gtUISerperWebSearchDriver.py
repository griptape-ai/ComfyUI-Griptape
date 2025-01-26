from griptape.serper.drivers.serper_web_search.driver import SerperWebSearchDriver

from ...py.griptape_settings import GriptapeSettings
from .gtUIBaseWebSearchDriver import gtUIBaseWebSearchDriver

search_types = ["all", "news", "places", "images", "patents"]
date_ranges = [
    "all",
    "past hour",
    "past 24 hours/day",
    "past week",
    "past month",
    "past year",
]


class gtUISerperWebSearchDriver(gtUIBaseWebSearchDriver):
    DESCRIPTION = "Serper Web Search Driver. To use the driver you'll need an API key from https://serper.dev/"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "search_type": (
                    search_types,
                    {
                        "default": search_types[0],
                        "tooltip": "Type of web search to complete",
                    },
                ),
                "date_range": (
                    date_ranges,
                    {
                        "default": date_ranges[0],
                        "tooltip": "Optional date range for search",
                    },
                ),
            },
        }

    def create(self, **kwargs):
        settings = GriptapeSettings()
        api_key = settings.get_settings_key_or_use_env("SERPER_API_KEY")

        params = {}
        search = kwargs.get("search_type", search_types[0])
        date = kwargs.get("date_range", date_ranges[0])

        if not search == "all":
            params["type"] = search

        if not date == "all":
            if date == "past hour":
                date_range = "h"
            elif date == "past 24 hours/day":
                date_range = "d"
            elif date == "past week":
                date_range = "w"
            elif date == "past month":
                date_range = "m"
            elif date == "past year":
                date_range = "y"
            params["date_range"] = date_range
        driver = SerperWebSearchDriver(api_key=api_key, **params)
        return (driver,)
