from griptape.drivers import GoogleWebSearchDriver

from ...py.griptape_config import get_config
from .BaseWebSearchDriver import gtUIBaseWebSearchDriver


class gtUIGoogleWebSearchDriver(gtUIBaseWebSearchDriver):
    DESCRIPTION = "Google Web Search Driver. Requires environment variables GOOGLE_API_KEY and GOOGLE_API_SEARCH_ID."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "country": ("STRING", {"default": "us"}),
                "language": ("STRING", {"default": "en"}),
                "results_count": ("INT", {"default": 5}),
            }
        )
        return inputs

    def get_api_key(self, KEY_ID):
        # will get the API key from the environment, or return the default value
        return get_config(key=KEY_ID, default=None)

    def create(self, language="en", country="us", results_count=5):
        GOOGLE_API_KEY = self.get_api_key("env.GOOGLE_API_KEY")
        GOOGLE_API_SEARCH_ID = self.get_api_key("env.GOOGLE_API_SEARCH_ID")

        if not GOOGLE_API_KEY:
            raise Exception(
                "Google API Key not found. Please set the environment variable GOOGLE_API_KEY."
            )
        if not GOOGLE_API_SEARCH_ID:
            raise Exception(
                "Google API Search ID not found. Please set the environment variable GOOGLE_API_SEARCH_ID."
            )
        driver = GoogleWebSearchDriver(
            api_key=GOOGLE_API_KEY,
            search_id=GOOGLE_API_SEARCH_ID,
            country=country,
            language=language,
            results_count=results_count,
        )
        return (driver,)
