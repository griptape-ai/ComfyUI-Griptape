from dotenv import load_dotenv
from griptape.drivers import TavilyWebSearchDriver

from .gtUIBaseWebSearchDriver import gtUIBaseWebSearchDriver

load_dotenv()
DEFAULT_API_KEY_ENV_VAR = "TAVILY_API_KEY"


class gtUITavilyWebSearchDriver(gtUIBaseWebSearchDriver):
    DESCRIPTION = (
        "Tavily Web Search Driver. Requires environment variables TAVILY_API_KEY."
    )

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "search_depth": (
                    ["basic", "advanced"],
                    {"default": "basic", "tooltip": "The depth of the search"},
                ),
                "topic": (
                    ["general", "news"],
                    {"default": "general", "tooltop": "The category of the search"},
                ),
                "days": (
                    "INT",
                    {
                        "default": 3,
                        "tooltip": "The number of days back from the current date to include in the search results.\nOnly when using 'news' search topic.",
                    },
                ),
                "max_results": (
                    "INT",
                    {
                        "default": 5,
                        "tooltip": "The maximum number of search results to return.",
                    },
                ),
                "include_answer": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "include a short answer to the search query",
                    },
                ),
                "include_raw_content": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "include the cleaned and parsed HTML content",
                    },
                ),
                "include_domains": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "A list of domains to include in the search results",
                    },
                ),
                "exclude_domains": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "A list of domains to exclude from the search results",
                    },
                ),
            }
        )
        inputs["optional"].update(
            {
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV_VAR,
                        "tooltip": "The name of the environment variable that contains the API key. Do not include the actual API key here.",
                    },
                ),
            }
        )
        return inputs

    def create(self, **kwargs):
        search_depth = kwargs.get("search_depth", "basic")
        topic = kwargs.get("topic", "general")
        days = kwargs.get("days", 3)
        max_results = kwargs.get("max_results", 5)
        include_answer = kwargs.get("include_answer", False)
        include_raw_content = kwargs.get("include_raw_content", False)
        include_domains = kwargs.get("include_domains", None)
        exclude_domains = kwargs.get("exclude_domains", None)

        TAVILY_API_KEY = self.getenv(
            kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        )

        if not TAVILY_API_KEY:
            raise Exception(
                "Tavily API Key not found. Please set the environment variable TAVILY_API_KEY."
            )

        tavily_params = {}
        addl_params = {}
        addl_params["search_depth"] = search_depth
        addl_params["topic"] = topic
        if topic == "news":
            addl_params["days"] = days
        tavily_params["results_count"] = max_results
        addl_params["include_answer"] = include_answer
        addl_params["include_raw_content"] = include_raw_content
        if include_domains:
            addl_params["include_domains"] = include_domains.split("\n")
        if exclude_domains:
            addl_params["exclude_domains"] = exclude_domains.split("\n")

        if TAVILY_API_KEY:
            tavily_params["api_key"] = TAVILY_API_KEY

        driver = TavilyWebSearchDriver(**tavily_params, params=addl_params)
        return (driver,)
