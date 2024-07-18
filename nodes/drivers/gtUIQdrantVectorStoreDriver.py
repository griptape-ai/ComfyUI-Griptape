import os

from griptape.drivers import OpenAiEmbeddingDriver, QdrantVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()


default_api_key_env = "QDRANT_CLUSTER_API_KEY"
default_url_env = "QDRANT_CLUSTER_ENDPOINT"
default_collection_name = "griptape"
default_payload_key = "content"


class gtUIQdrantVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Qdrant Vector Store Driver: https://qdrant.tech/"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "api_key_env": ("STRING", {"default": default_api_key_env}),
                "url_env": ("STRING", {"default": default_url_env}),
                "collection_name": ("STRING", {"default": default_collection_name}),
                "content_payload_key": ("STRING", {"default": default_payload_key}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        url_env = kwargs.get("url_env", default_url_env)
        api_key_env = kwargs.get("api_key_env", default_api_key_env)
        collection_name = kwargs.get("collection_name", default_collection_name)
        content_payload_key = kwargs.get("content_payload_key", default_payload_key)

        if url_env:
            url = os.getenv(url_env)
        if api_key_env:
            api_key = os.getenv(api_key_env)

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
