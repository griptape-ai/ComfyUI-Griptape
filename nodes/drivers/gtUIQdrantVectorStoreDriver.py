from griptape.drivers import OpenAiEmbeddingDriver, QdrantVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()


DEFAULT_API_KEY_ENV = "QDRANT_CLUSTER_API_KEY"
DEFAULT_URL_ENV = "QDRANT_CLUSTER_ENDPOINT"
DEFAULT_COLLECTION_NAME = "griptape"
DEFAULT_PAYLOAD_KEY = "content"


class gtUIQdrantVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Qdrant Vector Store Driver: https://qdrant.tech/"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "api_key_env": ("STRING", {"default": DEFAULT_API_KEY_ENV}),
                "url_env": ("STRING", {"default": DEFAULT_URL_ENV}),
                "collection_name": ("STRING", {"default": DEFAULT_COLLECTION_NAME}),
                "content_payload_key": ("STRING", {"default": DEFAULT_PAYLOAD_KEY}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        url_env = kwargs.get("url_env", DEFAULT_URL_ENV)
        api_key_env = kwargs.get("api_key_env", DEFAULT_API_KEY_ENV)
        collection_name = kwargs.get("collection_name", DEFAULT_COLLECTION_NAME)
        content_payload_key = kwargs.get("content_payload_key", DEFAULT_PAYLOAD_KEY)

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
            params["embedding_driver"] = default_embedding_driver
        driver = QdrantVectorStoreDriver(**params)
        return (driver,)
