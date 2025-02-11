from griptape.drivers.vector.qdrant import QdrantVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

DEFAULT_API_KEY_ENV = "QDRANT_CLUSTER_API_KEY"
DEFAULT_URL_ENV = "QDRANT_CLUSTER_ENDPOINT"
DEFAULT_COLLECTION_NAME = "griptape"
DEFAULT_PAYLOAD_KEY = "content"


class gtUIQdrantVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Qdrant Vector Store Driver: https://qdrant.tech/"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "collection_name": (
                    "STRING",
                    {
                        "default": DEFAULT_COLLECTION_NAME,
                        "tooltip": "Name of the Qdrant collection",
                    },
                ),
                "content_payload_key": (
                    "STRING",
                    {
                        "default": DEFAULT_PAYLOAD_KEY,
                        "tooltip": "Key for the content payload",
                    },
                ),
                "api_key_env": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV,
                        "tooltip": "Environment variable name for the API key (do not include the actual API key)",
                    },
                ),
                "url_env": (
                    "STRING",
                    {
                        "default": DEFAULT_URL_ENV,
                        "tooltip": "Environment variable name for the Qdrant cluster endpoint URL",
                    },
                ),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)
        url_env = kwargs.get("url_env", DEFAULT_URL_ENV)
        api_key_env = kwargs.get("api_key_env", DEFAULT_API_KEY_ENV)
        collection_name = kwargs.get("collection_name", DEFAULT_COLLECTION_NAME)
        content_payload_key = kwargs.get("content_payload_key", DEFAULT_PAYLOAD_KEY)

        url = None
        api_key = None

        if url_env:
            url = self.getenv(url_env)
        if api_key_env:
            api_key = self.getenv(api_key_env)

        params = {}

        if api_key:
            params["api_key"] = api_key
        if url:
            params["url"] = url
        if collection_name:
            params["collection_name"] = collection_name
        if content_payload_key:
            params["content_payload_key"] = content_payload_key
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()
        driver = QdrantVectorStoreDriver(**params)
        return (driver,)
