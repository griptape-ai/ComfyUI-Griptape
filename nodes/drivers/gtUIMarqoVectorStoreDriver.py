from griptape.drivers import (
    MarqoVectorStoreDriver,
)

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

DEFAULT_API_KEY_ENV = "MARQO_API_KEY"
DEFAULT_INDEX_NAME_ENV = "MARQO_INDEX_NAME"
DEFAULT_URL_ENV = "MARQO_URL"


class gtUIMarqoVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Marqo Vector Store Driver: https://www.marqo.ai/"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV,
                        "tooltip": "Environment variable for the API key. Do not use your actual API key here.",
                    },
                ),
                "url_env": (
                    "STRING",
                    {
                        "default": DEFAULT_URL_ENV,
                        "tooltip": "Environment variable for the Marqo URL. ",
                    },
                ),
                "index_name_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_INDEX_NAME_ENV,
                        "tooltip": "Environment variable for the Marqo index name.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV))
        url_env = self.getenv(kwargs.get("environment_env_var", DEFAULT_URL_ENV))
        index_name_env_var = self.getenv(
            kwargs.get("index_name_env_var", DEFAULT_INDEX_NAME_ENV)
        )

        params = {
            "api_key": api_key,
            "environment": url_env,
            "index_name": index_name_env_var,
        }
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = MarqoVectorStoreDriver(**params)
        return (driver,)
