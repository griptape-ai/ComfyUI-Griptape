import os

from griptape.drivers import AmazonOpenSearchVectorStoreDriver, OpenAiEmbeddingDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()

default_host_env = "AMAZON_OPENSEARCH_HOST"
default_index_env = "AMAZON_OPENSEARCH_INDEX_NAME"


class gtUIAmazonOpenSearchVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Open Search Vector Store Driver: https://aws.amazon.com/opensearch-service/"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "host_env": ("STRING", {"default": default_host_env}),
                "index_env": ("STRING", {"default": default_index_env}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        host_env = kwargs.get("host_env", default_host_env)
        index_env_var = kwargs.get("index_name_env", default_index_env)

        if host_env:
            host = os.getenv(host_env)
        if index_env_var:
            index = os.getenv(index_env_var)
        params = {}
        if host:
            params["host"] = host
        if index:
            params["index_name"] = index
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = default_embedding_driver
        driver = AmazonOpenSearchVectorStoreDriver(**params)
        return (driver,)
