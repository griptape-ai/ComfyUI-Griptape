from griptape.drivers.embedding.cohere import CohereEmbeddingDriver

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

DEFAULT_API_KEY_ENV_VAR = "COHERE_API_KEY"
models = ["embed-english-v3.0", "embed-multilingual-v3.0"]
input_types = ["search_query", "search_document", "classification"]


class gtUICohereEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "Cohere Embedding Driver"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["required"].update()
        inputs["optional"].update(
            {
                "embedding_model": (
                    models,
                    {
                        "default": models[0],
                        "tooltip": "Select the embedding model to use.",
                    },
                ),
                "input_types": (
                    input_types,
                    {
                        "default": input_types[0],
                        "tooltip": "Select the type of input for embedding.",
                    },
                ),
                "cohere_api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV_VAR,
                        "tooltip": "Environment variable name for the Cohere API key. Do not enter your actual API key.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        api_key = self.getenv(
            kwargs.get("cohere_api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        )
        model = kwargs.get("embedding_model", models[0])
        input_type = kwargs.get("input_types", input_types[0])
        params = {
            "api_key": api_key,
            "model": model,
            "input_type": input_type,
        }
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = CohereEmbeddingDriver(**params)
        return (driver,)
