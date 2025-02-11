from griptape.drivers.embedding.google import GoogleEmbeddingDriver

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

models = [
    "text-embedding-004",
]
task_types = [
    "RETRIEVAL_QUERY",
    "RETRIEVAL_DOCUMENT",
    "SEMANTIC_SIMILARITY",
    "CLASSIFICATION",
    "CLUSTERING	",
]
DEFAULT_API_KEY_ENV_VAR = "GOOGLE_API_KEY"


class gtUIGoogleEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "Google Embedding Driver"

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
                "task_type": (
                    task_types,
                    {
                        "default": task_types[0],
                        "tooltip": "Select the task type for the embedding.",
                    },
                ),
                "google_api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV_VAR,
                        "tooltip": "Environment variable for the Google API key. Do not use your actual API key here.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        api_key = self.getenv(
            kwargs.get("google_api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        )
        model = kwargs.get("embedding_model", models[0])
        task_type = kwargs.get("task_type", task_types[0])

        params = {
            "api_key": api_key,
            "model": model,
            "task_type": task_type,
        }
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        driver = GoogleEmbeddingDriver(**params)
        return (driver,)
