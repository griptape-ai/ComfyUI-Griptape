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
                "api_key_env_var": ("STRING", {"default": DEFAULT_API_KEY_ENV}),
                "url_env": ("STRING", {"default": DEFAULT_URL_ENV}),
                "index_name_env_var": ("STRING", {"default": DEFAULT_INDEX_NAME_ENV}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV)
        url_env = kwargs.get("environment_env_var", DEFAULT_URL_ENV)
        index_name_env_var = kwargs.get("index_name_env_var", DEFAULT_INDEX_NAME_ENV)

        params = {}
        if api_key_env_var:
            params["api_key"] = self.getenv(api_key_env_var)
        if url_env:
            params["environment"] = self.getenv(DEFAULT_URL_ENV)
        if index_name_env_var:
            params["index_name"] = self.getenv(index_name_env_var)
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()
        driver = MarqoVectorStoreDriver(**params)
        return (driver,)
