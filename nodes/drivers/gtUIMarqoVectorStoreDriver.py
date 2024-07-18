import os

from griptape.drivers import MarqoVectorStoreDriver, OpenAiEmbeddingDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()

default_api_key_env = "MARQO_API_KEY"
default_index_name_env = "MARQO_INDEX_NAME"
default_url_env = "MARQO_URL"


class gtUIMarqoVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Marqo Vector Store Driver: https://www.marqo.ai/"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "api_key_env_var": ("STRING", {"default": default_api_key_env}),
                "url_env": ("STRING", {"default": default_url_env}),
                "index_name_env_var": ("STRING", {"default": default_index_name_env}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        api_key_env_var = kwargs.get("api_key_env_var", default_api_key_env)
        url_env = kwargs.get("environment_env_var", default_url_env)
        index_name_env_var = kwargs.get("index_name_env_var", default_index_name_env)

        params = {}
        if api_key_env_var:
            params["api_key"] = os.getenv(api_key_env_var)
        if url_env:
            params["environment"] = os.getenv(default_url_env)
        if index_name_env_var:
            params["index_name"] = os.getenv(index_name_env_var)
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = default_embedding_driver
        driver = MarqoVectorStoreDriver(**params)
        return (driver,)
