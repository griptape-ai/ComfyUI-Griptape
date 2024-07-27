from griptape.drivers import AzureOpenAiEmbeddingDriver

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
DEFAULT_API_KEY_ENV_VAR = "AZURE_OPENAI_API_KEY"
DEFAULT_AZURE_ENDPOINT_ENV_VAR = "AZURE_OPENAI_ENDPOINT"


class gtUIAzureOpenAiEmbeddingDriver(gtUIBaseEmbeddingDriver):
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
                    {"default": DEFAULT_AZURE_ENDPOINT_ENV_VAR},
                ),
                "api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_API_KEY_ENV_VAR},
                ),
            }
        )

        return inputs

    def create(self, **kwargs):
        model = kwargs.get("model", models[0])
        azure_endpoint_env_var = kwargs.get("base_url", DEFAULT_AZURE_ENDPOINT_ENV_VAR)
        api_key_env_var = kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR)

        params = {}

        if model:
            params["model"] = model
        if azure_endpoint_env_var:
            params["azure_endpoint"] = self.getenv(azure_endpoint_env_var)
        if api_key_env_var:
            params["api_key"] = self.getenv(api_key_env_var)
        driver = AzureOpenAiEmbeddingDriver(**params)
        return (driver,)
