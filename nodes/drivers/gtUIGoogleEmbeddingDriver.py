from griptape.drivers import GoogleEmbeddingDriver

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

models = [
    "models/embedding-001",
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
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "model": (
                    models,
                    {"default": models[0]},
                ),
                "task_type": (
                    task_types,
                    {"default": task_types[0]},
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
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY_ENV_VAR))
        task_type = kwargs.get("task_type", task_types[0])

        params = {}

        if model:
            params["model"] = model
        if task_type:
            params["task_type"] = task_type
        if api_key:
            params["api_key"] = api_key

        driver = GoogleEmbeddingDriver(**params)
        return (driver,)
