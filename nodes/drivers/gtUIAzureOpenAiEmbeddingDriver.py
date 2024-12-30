from griptape.drivers import AzureOpenAiEmbeddingDriver

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
DEFAULT_API_KEY_ENV_VAR = "AZURE_OPENAI_API_KEY"
DEFAULT_AZURE_ENDPOINT_ENV_VAR = "AZURE_OPENAI_ENDPOINT"


class gtUIAzureOpenAiEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "Azure OpenAI Embedding Driver"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["required"].update()
        inputs["optional"].update(
            {
                "embedding_model": (
                    models,
                    {"default": models[0]},
                ),
                "endpoint_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_AZURE_ENDPOINT_ENV_VAR,
                        "tooltip": "Enter the name of the environment variable for AZURE_OPENAI_ENDPOINT, not the actual endpoint.",
                    },
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV_VAR,
                        "tooltip": "Enter the name of the environment variable for AZURE_OPENAI_API_KEY, not the actual API key.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        model = kwargs.get("embedding_model", None)
        azure_endpoint = self.getenv(
            kwargs.get("base_url", DEFAULT_AZURE_ENDPOINT_ENV_VAR)
        )
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR))

        params = {
            "azure_endpoint": azure_endpoint,
            "api_key": api_key,
            "model": model,
        }

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = AzureOpenAiEmbeddingDriver(**params)
        return (driver,)
