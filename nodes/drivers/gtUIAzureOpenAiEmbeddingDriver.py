import os

from griptape.drivers import AzureOpenAiEmbeddingDriver

from .gtUIBaseDriver import gtUIBaseDriver

models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
default_api_key_env_var = "AZURE_OPENAI_API_KEY"
default_azure_endpoint_env_var = "AZURE_OPENAI_ENDPOINT"


class gtUIAzureOpenAiEmbeddingDriver(gtUIBaseDriver):
    DESCRIPTION = "Azure OpenAI Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "model": (
                    models,
                    {"default": models[0]},
                ),
                "endpoint_env_var": (
                    "STRING",
                    {"default": default_azure_endpoint_env_var},
                ),
                "api_key_env_var": (
                    "STRING",
                    {"default": default_api_key_env_var},
                ),
            }
        )

        return inputs

    CATEGORY = "Griptape/Drivers/Embedding"

    def create(self, **kwargs):
        model = kwargs.get("model", models[0])
        azure_endpoint_env_var = kwargs.get("base_url", default_azure_endpoint_env_var)
        api_key_env_var = kwargs.get("api_key_env_var", default_api_key_env_var)

        params = {}

        if model:
            params["model"] = model
        if azure_endpoint_env_var:
            params["azure_endpoint"] = os.getenv(azure_endpoint_env_var)
        if api_key_env_var:
            params["api_key"] = os.getenv(api_key_env_var)
        driver = AzureOpenAiEmbeddingDriver(**params)
        return (driver,)
