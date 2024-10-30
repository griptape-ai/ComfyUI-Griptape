from griptape.drivers import DummyEmbeddingDriver, VoyageAiEmbeddingDriver

from .gtUIBaseEmbeddingDriver import gtUIBaseEmbeddingDriver

DEFAULT_API_KEY_ENV_VAR = "VOYAGE_API_KEY"


class gtUIVoyageAiEmbeddingDriver(gtUIBaseEmbeddingDriver):
    DESCRIPTION = "Voyage AI Embedding Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()

        # Get the base required and optional inputs
        base_required_inputs = inputs["required"]
        base_optional_inputs = inputs["optional"]

        # Add the base required inputs to the inputs
        inputs["required"].update(base_required_inputs)

        # Add the optional inputs
        inputs["optional"].update(base_optional_inputs)
        inputs["optional"].update(
            {
                "voyage_api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY_ENV_VAR,
                        "tooltip": "Environment variable name for the Voyage API key (do not include the actual API key)",
                    },
                ),
                "embedding_model": (
                    "STRING",
                    {
                        "default": "voyage-large-2",
                        "tooltip": "The model to use for embedding",
                    },
                ),
                "input_type": (
                    "STRING",
                    {
                        "default": "document",
                        "tooltip": "The type of input to embed (e.g., document, text)",
                    },
                ),
                "ignore_voyage_embedding_driver": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Whether to ignore the Voyage AI Embedding Driver and use a dummy driver instead",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        api_key = self.getenv(
            kwargs.get("voyage_api_key_env_var", DEFAULT_API_KEY_ENV_VAR)
        )
        model = kwargs.get("embedding_model", "voyage-large-2")
        input_type = kwargs.get("input_type", "document")
        ignore = kwargs.get("ignore_voyage_embedding_driver", False)
        if ignore:
            params = {
                "api_key": api_key,
                "model": model,
                "input_type": input_type,
            }
        else:
            params = {}
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        if params == {}:
            driver = DummyEmbeddingDriver()
        else:
            driver = VoyageAiEmbeddingDriver(**params)
        return (driver,)
