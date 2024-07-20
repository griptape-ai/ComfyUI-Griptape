from griptape.drivers import OpenAiEmbeddingDriver, PineconeVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()

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
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY_ENV}),
                "environment_env_var": ("STRING", {"default": DEFAULT_ENVIRONMENT_ENV}),
                "index_name_env_var": ("STRING", {"default": DEFAULT_INDEX_NAME_ENV}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV)
        environment_env_var = kwargs.get("environment_env_var", DEFAULT_ENVIRONMENT_ENV)
        index_name_env_var = kwargs.get("index_name_env_var", DEFAULT_INDEX_NAME_ENV)

        params = {}
        if api_key_env_var:
            params["api_key"] = self.getenv(api_key_env_var)
        if environment_env_var:
            params["environment"] = self.getenv(environment_env_var)
        if index_name_env_var:
            params["index_name"] = self.getenv(index_name_env_var)
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = default_embedding_driver
        driver = PineconeVectorStoreDriver(**params)
        return (driver,)
