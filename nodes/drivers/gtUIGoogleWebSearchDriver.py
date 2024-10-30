from griptape.drivers import GoogleWebSearchDriver

from .gtUIBaseWebSearchDriver import gtUIBaseWebSearchDriver

DEFAULT_API_KEY_ENV_VAR = "GOOGLE_API_KEY"
DEFAULT_GOOGLE_API_SEARCH_ID = "GOOGLE_API_SEARCH_ID"


class gtUIGoogleWebSearchDriver(gtUIBaseWebSearchDriver):
    DESCRIPTION = "Google Web Search Driver. Requires environment variables GOOGLE_API_KEY and GOOGLE_API_SEARCH_ID."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "country": (
                    "STRING",
                    {
                        "default": "us",
                        "tooltip": "Country code for the search results.",
                    },
                ),
                "language": (
                    "STRING",
                    {
                        "default": "en",
                        "tooltip": "Language code for the search results.",
                    },
                ),
                "results_count": (
                    "INT",
                    {"default": 5, "tooltip": "Number of search results to return."},
                ),
            }
        )
        inputs["optional"].update(
            {
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV_VAR,
                        "tooltip": "Environment variable name for the Google API key. Do not use your actual API key here.",
                    },
                ),
                "search_id_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_GOOGLE_API_SEARCH_ID,
                        "tooltip": "Environment variable name for the Google API Search ID. Do not use your actual API Search ID here.",
                    },
                ),
            }
        )
        return inputs

    def create(self, **kwargs):
        language = kwargs.get("language", "en")
        country = kwargs.get("country", "us")
        results_count = kwargs.get("results_count", 5)

        GOOGLE_API_KEY = self.getenv(
            kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        )
        GOOGLE_API_SEARCH_ID = self.getenv(
            kwargs.get("search_id_env_var", DEFAULT_GOOGLE_API_SEARCH_ID)
        )

        if not GOOGLE_API_KEY:
            raise Exception(
                "Google API Key not found. Please set the environment variable GOOGLE_API_KEY."
            )
        if not GOOGLE_API_SEARCH_ID:
            raise Exception(
                "Google API Search ID not found. Please set the environment variable GOOGLE_API_SEARCH_ID."
            )

        params = {}
        if language:
            params["language"] = language
        if country:
            params["country"] = country
        if results_count:
            params["results_count"] = results_count
        if GOOGLE_API_KEY:
            params["api_key"] = GOOGLE_API_KEY
        if GOOGLE_API_SEARCH_ID:
            params["search_id"] = GOOGLE_API_SEARCH_ID

        driver = GoogleWebSearchDriver(**params)
        return (driver,)
