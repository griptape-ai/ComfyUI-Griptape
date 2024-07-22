import os

from griptape.drivers import (
    AmazonOpenSearchVectorStoreDriver,
)

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

DEFAULT_HOST_ENV = "AMAZON_OPENSEARCH_HOST"
DEFAULT_INDEX_ENV = "AMAZON_OPENSEARCH_INDEX_NAME"
DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


class gtUIAmazonOpenSearchVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Open Search Vector Store Driver: https://aws.amazon.com/opensearch-service/"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "host_env": ("STRING", {"default": DEFAULT_HOST_ENV}),
                "index_env": ("STRING", {"default": DEFAULT_INDEX_ENV}),
                "aws_access_key_id_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_ACCESS_KEY_ID},
                ),
                "aws_secret_access_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_SECRET_ACCESS_KEY},
                ),
                "aws_default_region_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_DEFAULT_REGION},
                ),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)
        host_env = kwargs.get("host_env", DEFAULT_HOST_ENV)
        index_env_var = kwargs.get("index_name_env", DEFAULT_INDEX_ENV)

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
            params["embedding_driver"] = self.get_default_embedding_driver()
        driver = AmazonOpenSearchVectorStoreDriver(**params)
        return (driver,)
