import os

from griptape.drivers import OpenAiEmbeddingDriver, PineconeVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()

default_api_key_env = "PINECONE_API_KEY"
default_environment_env = "PINECONE_ENVIRONMENT"
default_index_name_env = "PINECONE_INDEX_NAME"


class gtUIPineconeVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Pinecone Vector Store Driver: https://www.pinecone.io/"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "api_key_env_var": ("STRING", {"default": default_api_key_env}),
                "environment_env_var": ("STRING", {"default": default_environment_env}),
                "index_name_env_var": ("STRING", {"default": default_index_name_env}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        api_key_env_var = kwargs.get("api_key_env_var", default_api_key_env)
        environment_env_var = kwargs.get("environment_env_var", default_environment_env)
        index_name_env_var = kwargs.get("index_name_env_var", default_index_name_env)

        params = {}
        if api_key_env_var:
            params["api_key"] = os.getenv(api_key_env_var)
        if environment_env_var:
            params["environment"] = os.getenv(environment_env_var)
        if index_name_env_var:
            params["index_name"] = os.getenv(index_name_env_var)
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = default_embedding_driver
        driver = PineconeVectorStoreDriver(**params)
        return (driver,)
