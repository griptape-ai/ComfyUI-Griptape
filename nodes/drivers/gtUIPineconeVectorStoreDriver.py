from griptape.drivers import PineconeVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

DEFAULT_API_KEY_ENV = "PINECONE_API_KEY"
DEFAULT_ENVIRONMENT_ENV = "PINECONE_ENVIRONMENT"
DEFAULT_INDEX_NAME_ENV = "PINECONE_INDEX_NAME"


class gtUIPineconeVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Pinecone Vector Store Driver: https://www.pinecone.io/"

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
                        "tooltip": "Environment variable name for the API key. Do not include the actual API key.",
                    },
                ),
                "environment_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_ENVIRONMENT_ENV,
                        "tooltip": "Environment variable name for the Pinecone environment.",
                    },
                ),
                "index_name_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_INDEX_NAME_ENV,
                        "tooltip": "Environment variable name for the Pinecone index name.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV))
        environment = self.getenv(
            kwargs.get("environment_env_var", DEFAULT_ENVIRONMENT_ENV)
        )
        index_name = self.getenv(
            kwargs.get("index_name_env_var", DEFAULT_INDEX_NAME_ENV)
        )

        params = {
            "api_key": api_key,
            "environment": environment,
            "index_name": index_name,
        }
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        driver = PineconeVectorStoreDriver(**params)
        return (driver,)
