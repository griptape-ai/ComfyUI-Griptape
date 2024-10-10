from dotenv import load_dotenv
from griptape.drivers import ExaWebSearchDriver

from .gtUIBaseWebSearchDriver import gtUIBaseWebSearchDriver

load_dotenv()
DEFAULT_API_KEY_ENV_VAR = "EXA_API_KEY"


class gtUIExaWebSearchDriver(gtUIBaseWebSearchDriver):
    DESCRIPTION = "Exa Web Search Driver. Requires environment variables EXA_API_KEY."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "type": (
                    ["keyword", "neural", "auto"],
                    {"default": "neural", "tooltip": "The type of search"},
                ),
                "highlights": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Extracts relevant excerpts or highlights from retrieved content.",
                    },
                ),
                "use_autoprompt": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "If true, your query will be converted to a Exa query. Default false. Neural or Auto search only.",
                    },
                ),
                "category": (
                    [
                        "none",
                        "company",
                        "research paper",
                        "news",
                        "github",
                        "tweet",
                        "movie",
                        "song",
                        "personal site",
                        "pdf",
                    ],
                    {
                        "default": "none",
                        "tooltop": "(beta) A data category to focus on, with higher comprehensitivity and cleanliness.)",
                    },
                ),
                "num_results": (
                    "INT",
                    {
                        "default": 10,
                        "tooltip": "The maximum number of search results to return.",
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
                "include_text": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "A list of words to include in the search results",
                    },
                ),
                "exclude_text": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "A list of words to exclude from the search results",
                    },
                ),
            }
        )
        inputs["optional"].update(
            {
                "api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY_ENV_VAR},
                ),
            }
        )
        return inputs

    def create(self, **kwargs):
        highlights = kwargs.get("highlights", False)
        type = kwargs.get("type", "neural")
        use_autoprompt = kwargs.get("use_autoprompt", False)
        category = kwargs.get("category", "none")
        num_results = kwargs.get("num_results", 10)
        include_domains = kwargs.get("include_domains", None)
        exclude_domains = kwargs.get("exclude_domains", None)
        include_text = kwargs.get("include_text", None)
        exclude_text = kwargs.get("exclude_text", None)

        EXA_API_KEY = self.getenv(
            kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        )

        if not EXA_API_KEY:
            raise Exception(
                "Exa API Key not found. Please set the environment variable EXA_API_KEY."
            )

        exa_params = {}
        addl_params = {}
        exa_params["highlights"] = highlights
        if not type == "keyword":
            exa_params["use_autoprompt"] = use_autoprompt
        exa_params["results_count"] = num_results
        addl_params["category"] = category
        addl_params["type"] = type
        if include_domains:
            addl_params["include_domains"] = include_domains
        if exclude_domains:
            addl_params["exclude_domains"] = exclude_domains
        if include_text.strip() != "":
            addl_params["include_text"] = include_text
        if exclude_text.strip() != "":
            addl_params["exclude_text"] = exclude_text

        if EXA_API_KEY:
            exa_params["api_key"] = EXA_API_KEY

        driver = ExaWebSearchDriver(**exa_params, params=addl_params)
        return (driver,)
