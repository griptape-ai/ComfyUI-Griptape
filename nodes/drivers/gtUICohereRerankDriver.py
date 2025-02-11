from griptape.drivers.rerank.cohere import CohereRerankDriver

from .gtUIBaseRerankDriver import gtUIBaseRerankDriver

DEFAULT_API_KEY_ENV_VAR = "COHERE_API_KEY"
models = ["rerank-english-v3.0", "rerank-multilingual-v3.0"]


class gtUICohereRerankDriver(gtUIBaseRerankDriver):
    DESCRIPTION = "Cohere Rerank Driver"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "models": (
                    models,
                    {
                        "default": models[0],
                        "tooltip": "Select the model to use for reranking.",
                    },
                ),
                "top_n": (
                    "INT",
                    {
                        "default": 5,
                        "tooltip": "Specify the number of top results to return.",
                    },
                ),
                "cohere_api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV_VAR,
                        "tooltip": "Environment variable name for the Cohere API key. Do not use your actual API key here.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        api_key = self.getenv(
            kwargs.get("cohere_api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        )
        model = kwargs.get("models", models[0])
        top_n = kwargs.get("top_n", 5)
        params = {
            "api_key": api_key,
            "model": model,
            "top_n": top_n,
        }
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        driver = CohereRerankDriver(**params)
        return (driver,)
